from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec, InputMultiPath
import os

class SVCInputSpec(BaseInterfaceInputSpec):
    in_file = traits.List(desc="all_subjects", mandatory=True)
    labels = traits.List(exists=True, desc="labels with phenotype values", mandatory=True)

class SVCOutputSpec(TraitedSpec):
    label_file = traits.File(exists=True, desc="labels of phenotype")
    data_paths = traits.File(exists=True, desc="paths for data")

class SVC(BaseInterface):
    input_spec = SVCInputSpec
    output_spec = SVCOutputSpec

    def _run_interface(self, runtime):
        #trainer = pe.Node(afni.SVMTrain(), name = 'Trainer')
        #trainer.inputs.ttype = 'regression'
        #trainer.inputs.options = '-c 100 -e 0.01 -overwrite'
        #trainer.inputs.max_iterations = 100
        with open('/home/rschadmin/Data/ADHDworking_dir/label_file', 'a+b') as f:
            f.write(str(self.inputs.labels)+'\n')
        with open('/home/rschadmin/Data/ADHDworking_dir/data_paths', 'a+b') as f:
            f.write(str(self.inputs.in_file)+'\n')
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs["label_file"] = os.path.abspath('/home/rschadmin/Data/ADHDworking_dir/label_file')
        outputs["data_paths"] = os.path.abspath('/home/rschadmin/Data/ADHDworking_dir/data_paths')
        return outputs
