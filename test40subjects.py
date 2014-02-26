from nipype import config
config.enable_debug_mode()

import nipype.pipeline.engine as pe
import nipype.pipeline.utils as util
import nipype.interfaces.io as nio
import nipype.interfaces.afni as afni
from nipype import JoinNode
import os
from text_out import Text_out
import numpy as np

from variables import workingdir, datadir, subjects, derivs, dg_template, dg_args

def get_wf():
    wf = pe.Workflow(name="svc_workflow")
    wf.base_dir = os.path.join(workingdir,"ADHD_npairs")
    wf.config['execution']['crashdump_dir'] = wf.base_dir + "/crash_files"

    #INFOSOURCE ITERABLES
    subject_id_infosource = pe.Node(util.IdentityInterface(fields=['subject_id']), name="subject_id_infosource")
    subject_id_infosource.iterables = [('subject_id', subjects)]

    #DATAGRABBER
    datagrabber = pe.Node(nio.DataGrabber(infields=['subject_id'], outfields=derivs), name='datagrabber')
    datagrabber.inputs.base_directory = datadir
    datagrabber.inputs.template='*'
    datagrabber.inputs.field_template = dg_template
    datagrabber.inputs.template_args= dg_args
    datagrabber.inputs.sort_filelist = True

    wf.connect(subject_id_infosource, 'subject_id', datagrabber, 'subject_id')

    #PHENOTYPER
    def get_pheno(subject_id):
        from variables import pheno_dict
        pheno_labels = pheno_dict.get(subject_id.lstrip("0"))
        return pheno_labels
        
    #OUTPUT PATHS & LABELS
    toText = pe.Node(Text_out(), name="alff")
    wf.connect(datagrabber, 'alff', toText, 'in_file')
    wf.connect(subject_id_infosource, ('subject_id', get_pheno), toText, 'labels')
    
    toText2 = pe.Node(Text_out(), name="falff")
    wf.connect(datagrabber, 'falff', toText2, 'in_file')
    wf.connect(subject_id_infosource, ('subject_id', get_pheno), toText2, 'labels')
         
    return wf
    
if __name__=='__main__':
    wf = get_wf()
    #wf.run(plugin="CondorDAGMan", plugin_args={"template":"universe = vanilla\nnotification = Error\ngetenv = true\nrequest_memory=4000"})
    #wf.run(plugin="MultiProc", plugin_args={"n_procs":16})
    wf.run(plugin="Linear", updatehash=True)  
