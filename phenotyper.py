from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec

class PhenotyperInputSpec(BaseInterfaceInputSpec):
    subject_id = traits.String(desc="subject")
    pheno_dict = traits.Dict(exists=True, desc="dictionary of phenotype values")

class PhenotyperOutputSpec(TraitedSpec):
    pheno_labels = traits.List(exists=True, desc="labels of phenotype")

class Phenotyper(BaseInterface):
    input_spec = PhenotyperInputSpec
    output_spec = PhenotyperOutputSpec

    def _run_interface(self, runtime):
        labels = pheno_dict.get(subject_id)
    return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs["pheno_labels"] = os.path.abspath('')
        return outputs
