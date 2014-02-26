from nipype import config
config.enable_debug_mode()

import nipype.pipeline.engine as pe
import nipype.pipeline.utils as util
import nipype.interfaces.utility as utility
import nipype.interfaces.io as nio
import nipype.interfaces.afni as afni
import os
from text_out import Text_out
import numpy as np

from variables import workingdir, datadir, subjects, derivs, preprocs

def get_wf():
    wf = pe.Workflow(name="svc_workflow")
    wf.base_dir = os.path.join(workingdir,"ADHD_npairs")
    wf.config['execution']['crashdump_dir'] = wf.base_dir + "/crash_files"

    #INFOSOURCE ITERABLES
    subject_id_infosource = pe.Node(util.IdentityInterface(fields=['subject_id']), name="subject_id_infosource")
    subject_id_infosource.iterables = [('subject_id', subjects)]
    
    deriv_id_infosource = pe.Node(util.IdentityInterface(fields=['deriv_id']), name="deriv_id_infosource")
    deriv_id_infosource.iterables = ('deriv_id', derivs)

    preproc_id_infosource = pe.Node(util.IdentityInterface(fields=['preproc_id']), name="preproc_id_infosource")
    preproc_id_infosource.iterables = ('preproc_id', preprocs)

    #DATAGRABBER
    datagrabber = pe.Node(nio.DataGrabber(infields=['subject_id','deriv_id','preproc_id'], outfields=derivs), name='datagrabber')
    datagrabber.inputs.base_directory = datadir
    datagrabber.inputs.template='%s*/%s/_scan_rest*/*/*/*/%s/*/*/*/*.nii.gz'
    datagrabber.inputs.template_args['deriv_files'] = [['subject_id', 'deriv_id','preproc_id']]
    datagrabber.inputs.sort_filelist = True

    wf.connect(subject_id_infosource, 'subject_id', datagrabber, 'subject_id')
    wf.connect(deriv_id_infosource, 'deriv_id', datagrabber, 'deriv_id')
    wf.connect(preproc_id_infosource, 'preproc_id', datagrabber, 'preproc_id')
    
    #OUTPUT PATHS & LABELS
    toText = pe.JoinNode(Text_out(), joinsource='subject_id_infosource', joinfield="in_file", name="text_files")
    
    wf.connect(datagrabber, 'deriv_files', toText, 'in_file')
         
    return wf
    
if __name__=='__main__':
    wf = get_wf()
    #wf.run(plugin="CondorDAGMan", plugin_args={"template":"universe = vanilla\nnotification = Error\ngetenv = true\nrequest_memory=4000"})
    #wf.run(plugin="MultiProc", plugin_args={"n_procs":16})
    wf.run(plugin="Linear", updatehash=True)  
