from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec, InputMultiPath
from variables import label_file, data_paths
import os

class Text_outInputSpec(BaseInterfaceInputSpec):
    in_file = traits.List(desc="fails for multiple files")
    labels = traits.List(exists=True, desc="labels with phenotype values", mandatory=True)

class Text_outOutputSpec(TraitedSpec):
    label_file = traits.File(exists=True, desc="labels of phenotype")
    data_paths = traits.File(exists=True, desc="paths for data")

class Text_out(BaseInterface):
    input_spec = Text_outInputSpec
    output_spec = Text_outOutputSpec
    
    def _run_interface(self, runtime):
        for x in self.inputs.in_file:
            with open(data_paths, 'a+b') as f:
                f.write(x+'\n')
            with open(label_file, 'a+b') as g:
                for y in self.inputs.labels:
                    g.write(y+',')
                g.write('\n')
            return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs["label_file"] = os.path.abspath(label_file)
        outputs["data_paths"] = os.path.abspath(data_paths)
        return outputs
