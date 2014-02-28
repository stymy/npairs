from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec, InputMultiPath
from variables import datadir, derivdir
import os

class Text_outInputSpec(BaseInterfaceInputSpec):
    in_file = traits.List(desc="multiple files in joinNode")

class Text_outOutputSpec(TraitedSpec):
    label_file = traits.File(exists=True, desc="labels of phenotype")
    data_paths = traits.File(exists=True, desc="paths for data")

class Text_out(BaseInterface):
    input_spec = Text_outInputSpec
    output_spec = Text_outOutputSpec
    
    #PHENOTYPER
    def get_pheno(self, path):
        from variables import pheno_dict
        subject_id = path.split('_session_1')[0].split('/')[-1] #find subject_id from path
        pheno_labels = pheno_dict.get(subject_id.lstrip("0")) #dict strips leading zeros
        return pheno_labels
    
    def _run_interface(self, runtime):
        for x in self.inputs.in_file:
            with open('paths', 'a+b') as f:
                f.write(x+'\n')
            with open('labels', 'a+b') as g:
                for y in self.get_pheno(x):
                    g.write(y+',')
                g.write('\n')
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs["label_file"] = os.path.abspath('labels')
        outputs["data_paths"] = os.path.abspath('paths')
        return outputs
