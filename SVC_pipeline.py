from nipype import config
config.enable_debug_mode()

import nipype.pipeline.engine as pe
import nipype.pipeline.utils as util
import nipype.interfaces.utility as utility
import nipype.interfaces.io as nio
import nipype.interfaces.afni as afni
import os
from text_out import Text_out
from classify import Classify
import numpy as np

from variables import workingdir, datadir, derivdir, subjects, derivs, preprocs, pprocs, methods, deriv_types

def get_wf():
    wf = pe.Workflow(name="svc_workflow")
    wf.base_dir = os.path.join(workingdir,"allNpairsSVC")
    wf.config['execution']['crashdump_dir'] = wf.base_dir + "/crash_files"

    #INFOSOURCE ITERABLES
    subject_id_infosource = pe.Node(util.IdentityInterface(fields=['subject_id']), name="subject_id_infosource")
    subject_id_infosource.iterables = [('subject_id', subjects)]

    method_id_infosource = pe.Node(util.IdentityInterface(fields=['method_id']), name="method_id_infosource")
    method_id_infosource.iterables = ('method_id', methods)
    
    deriv_id_infosource = pe.Node(util.IdentityInterface(fields=['deriv_id']), name="deriv_id_infosource")
    deriv_id_infosource.iterables = ('deriv_id', derivs)

    preproc_id_infosource = pe.Node(util.IdentityInterface(fields=['preproc_id']), name="preproc_id_infosource")
    preproc_id_infosource.iterables = ('preproc_id', preprocs)
    
    pproc_id_infosource = pe.Node(util.IdentityInterface(fields=['pproc_id']), name="pproc_id_infosource")
    pproc_id_infosource.iterables = ('pproc_id', pprocs)
    
    deriv_type_infosource = pe.Node(util.IdentityInterface(fields=['deriv_type']), name="deriv_type_infosource")
    deriv_type_infosource.iterables = ('deriv_type', deriv_types)

    #DATAGRABBER
    datagrabber = pe.Node(nio.DataGrabber(infields=['subject_id','deriv_id','preproc_id',
    'deriv_type','pproc_id'], outfields=['methods_files','centrality_files']), name='datagrabber')
    datagrabber.inputs.base_directory = '/'
    datagrabber.inputs.template = '*'
    datagrabber.inputs.field_template = dict(methods_files=os.path.join(datadir,'%s*/%s/_scan_rest*/*/*/*/%s/*/*/*/*.nii.gz'),
                                            centrality_files= os.path.join(derivdir,'%s/%s*/*zscore/*/%s/*%s*.nii.gz'))
    datagrabber.inputs.template_args = dict(methods_files= [['subject_id', 'method_id','preproc_id']],
                                            centrality_files= [['deriv_id','subject_id','pproc_id','deriv_type']])
    datagrabber.inputs.sort_filelist = True

    wf.connect(subject_id_infosource, 'subject_id', datagrabber, 'subject_id')
    wf.connect(deriv_id_infosource, 'deriv_id', datagrabber, 'deriv_id')
    wf.connect(deriv_type_infosource, 'deriv_type', datagrabber, 'deriv_type')
    wf.connect(method_id_infosource, 'method_id', datagrabber, 'method_id')  
    wf.connect(preproc_id_infosource, 'preproc_id', datagrabber, 'preproc_id')
    wf.connect(pproc_id_infosource, 'pproc_id', datagrabber, 'pproc_id')
    
    #OUTPUT PATHS & LABELS
    toText = pe.JoinNode(Text_out(), joinsource='subject_id_infosource', joinfield="in_file", name="methods_text_files")
    wf.connect(datagrabber, 'methods_files', toText, 'in_file')
    
    toText2 = pe.JoinNode(Text_out(), joinsource='subject_id_infosource', joinfield="in_file", name="eigen_cent_b_text_files")
    wf.connect(datagrabber, 'centrality_files', toText2, 'in_file')
    
    #RUN CLASSIFIERs
    classifier = pe.Node(Classify(), name='SVC_methods')
    wf.connect(toText, 'label_file', classifier, 'label_file')
    wf.connect(toText, 'data_paths', classifier, 'path_file')
    
    classifier2 = pe.Node(Classify(), name='SVC_eign_cent')
    wf.connect(toText2, 'label_file', classifier2, 'label_file')
    wf.connect(toText2, 'data_paths', classifier2, 'path_file') 
    
    #DATASINK
    
         
    return wf
    
if __name__=='__main__':
    wf = get_wf()
    #wf.run(plugin="CondorDAGMan", plugin_args={"template":"universe = vanilla\nnotification = Error\ngetenv = true\nrequest_memory=4000"})
    #wf.run(plugin="MultiProc", plugin_args={"n_procs":16})
    wf.run(plugin="Linear", updatehash=True)  
