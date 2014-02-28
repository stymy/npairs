import sys
nipype_path = "/home2/aimiwat/code/nipype-install/lib/python2.7/site-packages/"
sys.path.insert(0,nipype_path)
from nipype import config
cfg = dict(logging=dict(workflow_level = 'DEBUG'),
           execution={'stop_on_first_crash': True,
                      'hash_method': 'timestamp'})
config.update_config(cfg)

import nipype.pipeline.engine as pe
import nipype.pipeline.utils as util
import nipype.interfaces.utility as utility
import nipype.interfaces.io as nio
import nipype.interfaces.afni as afni
import os
from text_out import Text_out
from classify import Classify
import numpy as np

from variables import workingdir, datadir, outputdir, subjects, scans, preprocs

def get_wf():
    wf = pe.Workflow(name="svc_workflow")
    wf.base_dir = os.path.join(workingdir,"npairs_3deriv")
    wf.config['execution']['crashdump_dir'] = wf.base_dir + "/crash_files"

    #INFOSOURCE ITERABLES
    subject_id_infosource = pe.Node(util.IdentityInterface(fields=['subject_id']), name="subject_id_infosource")
    subject_id_infosource.iterables = [('subject_id', subjects)]
    
    scan_id_infosource = pe.Node(util.IdentityInterface(fields=['scan_id']), name= 'scan_id_infosource')
    scan_id_infosource.iterables = ('scan_id', scans)

    preproc_id_infosource = pe.Node(util.IdentityInterface(fields=['preproc_id']), name="preproc_id_infosource")
    preproc_id_infosource.iterables = ('preproc_id', preprocs)

    #DATAGRABBER
    datagrabber = pe.Node(nio.DataGrabber(infields=['subject_id', 'scan_id','preproc_id'], outfields=['falff_files','dr_files','reho_files','mask_file']), name='datagrabber')
    datagrabber.inputs.base_directory = '/'
    datagrabber.inputs.template = '*'
    datagrabber.inputs.field_template = dict(dr_files= os.path.join(datadir,'*%s*/dr_tempreg_maps_z_stack_to_standard/_scan_rest_%s_rest/*/*/*/%s/*/*.nii.gz'),
                                            reho_files= os.path.join(datadir,'*%s*/reho_Z_to_standard_smooth/_scan_rest_%s_rest/*/*/*/%s/*/*.nii.gz'),
                                            falff_files=os.path.join(datadir,'*%s*/falff_Z_to_standard_smooth/_scan_rest_%s_rest/*/*/*/%s/*/*/*/*.nii.gz'),
                                            mask_file = os.path.join(datadir,'*%s*/functional_brain_mask_to_standard/_scan_rest_%s_rest/*.nii.gz'))
                                            #centrality_files= os.path.join(derivdir,'%s/%s*/*zscore/*/%s/*%s*.nii.gz'),
                                            
    datagrabber.inputs.template_args = dict(falff_files= [['subject_id', 'scan_id','preproc_id']],
                                            reho_files= [['subject_id', 'scan_id','preproc_id']],
                                            dr_files= [['subject_id', 'scan_id','preproc_id']],
                                            mask_file= [['subject_id','scan_id']])
                                             #centrality_files= [['deriv_id','subject_id','pproc_id','deriv_type']],
                                           
    datagrabber.inputs.sort_filelist = True

    wf.connect(subject_id_infosource, 'subject_id', datagrabber, 'subject_id')
    wf.connect(scan_id_infosource, 'scan_id', datagrabber, 'scan_id')
    wf.connect(preproc_id_infosource, 'preproc_id', datagrabber, 'preproc_id')
    
    #CONCATENATE MASKS
    maskcat = pe.JoinNode(afni.TCat(), joinsource='subject_id_infosource', joinfield='in_files', name='maskcat')
    maskcat.inputs.terminal_output = 'file'
    maskcat.inputs.outputtype = 'NIFTI'
    wf.connect(datagrabber, 'mask_file', maskcat, 'in_files')

    #MEAN MASKS
    maskmerge = pe.Node(afni.TStat(), name='maskmerge')
    maskmerge.inputs.terminal_output = 'file'
    maskmerge.inputs.args='-mean'
    maskmerge.inputs.outputtype = 'NIFTI'
    wf.connect(maskcat, 'out_file', maskmerge, 'in_file')
    
    #THRESH MASKS to compute intersect of all subjects masks
    maskthresh = pe.Node(afni.Calc(), name='maskthresh')
    maskthresh.inputs.expr = 'ispositive(a-.97)'
    maskthresh.inputs.outputtype = 'NIFTI'
    wf.connect(maskmerge, 'out_file', maskthresh, 'in_file_a')
    
    #OUTPUT PATHS & LABELS
    toText = pe.JoinNode(Text_out(), joinsource='subject_id_infosource', joinfield="in_file", name="falff_text_files")
    wf.connect(datagrabber, 'falff_files', toText, 'in_file')

    
    toText2 = pe.JoinNode(Text_out(), joinsource='subject_id_infosource', joinfield="in_file", name="reho_text_files")
    wf.connect(datagrabber, 'reho_files', toText2, 'in_file')
    
    toText3 = pe.JoinNode(Text_out(), joinsource='subject_id_infosource', joinfield="in_file", name="dr_text_files")
    wf.connect(datagrabber, 'dr_files', toText3, 'in_file')
    
    #RUN CLASSIFIERs
    classifier = pe.Node(Classify(), name='SVC_falff')
    wf.connect(toText, 'label_file', classifier, 'label_file')
    wf.connect(toText, 'data_paths', classifier, 'path_file')
    wf.connect(maskthresh, 'out_file', classifier, 'mask_file')
    
    classifier2 = pe.Node(Classify(), name='SVC_reho')
    wf.connect(toText2, 'label_file', classifier2, 'label_file')
    wf.connect(toText2, 'data_paths', classifier2, 'path_file') 
    wf.connect(maskthresh, 'out_file', classifier2, 'mask_file')
    
    classifier3 = pe.Node(Classify(), name='SVC_dr')
    wf.connect(toText3, 'label_file', classifier3, 'label_file')
    wf.connect(toText3, 'data_paths', classifier3, 'path_file')
    wf.connect(maskthresh, 'out_file', classifier3, 'mask_file')
    
    #DATASINK
    ds = pe.Node(nio.DataSink(), name='datasink')
    ds.inputs.base_directory = outputdir
    
    wf.connect(classifier, 'pred', ds, 'prediction_accuracy_falff')
    wf.connect(classifier, 'rep', ds, 'reproducibility_falff')
    wf.connect(classifier2, 'pred', ds, 'prediction_accuracy_reho')
    wf.connect(classifier2, 'rep', ds, 'reproducibility_reho')
    wf.connect(classifier3, 'pred', ds, 'prediction_accuracy_dr')
    wf.connect(classifier3, 'rep', ds, 'reproducibility_dr')   
    
    wf.config['execution'] = {
                               'plugin': 'Linear',
                               'stop_on_first_rerun': 'False',
                               'hash_method': 'timestamp'}
    return wf
    
if __name__=='__main__':
    wf = get_wf()
    #wf.run(plugin="CondorDAGMan", plugin_args={"template":"universe = vanilla\nnotification = Error\ngetenv = true\nrequest_memory=4000"})
    #wf.run(plugin="MultiProc", plugin_args={"n_procs":16})
    wf.run(plugin="Linear")  
