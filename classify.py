from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec, InputMultiPath
import nibabel as nb
import numpy as np
from pyNPAIRS.core import NPAIRS
from sklearn import svm
from scipy.stats import ttest_ind
import os

class ClassifyInputSpec(BaseInterfaceInputSpec):
    label_file = traits.File(exists=True, desc="labels")
    path_file = traits.File(exists=True, desc="paths")
    mask_file = traits.File(exists=True, desc="brain_mask")

class ClassifyOutputSpec(TraitedSpec):
    pred = traits.File(desc="prediction accuracy")
    rep = traits.File(desc="reproducibility")
    
class Classify(BaseInterface):
    input_spec = ClassifyInputSpec
    output_spec = ClassifyOutputSpec
    
    def health(self,label,dx):
        boolean = not int(label[dx])==1
        return boolean

    def hand(self,label,H):
        try: handed = str(int(round(float(label[H]))))
        except ValueError:
            handed = label[H]
        return handed

    # create stratified and controlled splits
    def splitHalf(self,lbls,cnt,contlbls):
        
        # first we initialize our split 
        splits=np.ones((cnt,len(lbls)))

        # randomly generate cnt splits
        c = 0
        while c < cnt:
            tests=0
            tmp_splits = np.ones_like(splits[c])             
            for lbl in np.unique(lbls):
            
                # get the indices of the label
                lNdx = [i for i,x in enumerate(lbls) if x == lbl]
            
                # determine half of the number of the labels
                numL2 = int(round(lbls.count(lbl)/2.0))
                #import pdb; pdb.set_trace()
            
                lHalf = np.random.choice(lNdx,size=numL2,replace=False)
                tmp_splits[lHalf]=2
            # calculate ttest for each of the continuous varaibles you would like to control for
            for clbl in contlbls:
                a = np.array(clbl)[tmp_splits==1]
                b = np.array(clbl)[tmp_splits==2]
                try:ttest = ttest_ind(a,b)[1]
                except ZeroDivisionError:
                    import pdb; pdb.set_trace()
                print ttest
            # if all of the control variables are insignificant p > 0.5
                tests = tests+int(ttest>0.5)
            # and if haven't previously generated that split
            if tests == len(contlbls) and not any([all(tmp_splits == x) for x in splits]):
                splits[c] = tmp_splits
                tests = 0
                c=c+1
            else:
                continue

        return splits
                
    def _run_interface(self, runtime):
        labels=[]
        paths=[]
        with open(self.inputs.label_file, 'r') as f:
            for line in f:
                labels.append(line.strip().split(','))
        with open(self.inputs.path_file, 'r') as f:
            paths=[line.strip() for line in f]
            
        #ADHD
        #pheno_dict.get('ScanDir ID')
        #['ScanDir ID', 'Site', 'Gender', 'Age', 'Handedness', 'DX', 'Secondary Dx ', 'ADHD Measure', 'ADHD Index', 'Inattentive', 'Hyper/Impulsive', 'IQ Measure', 'Verbal IQ', 'Performance IQ', 'Full2 IQ', 'Full4 IQ', 'Med Status', 'QC_Rest_1', 'QC_Rest_2', 'QC_Rest_3', 'QC_Rest_4', 'QC_Anatomical_1', 'QC_Anatomical_2']

        #discrete labels
        #sex = 2
        #handedness = 4
        #site = 1
        #not_healthy = 5
        #continuous labels
        #meanFD = 3 #for now
        #age = 3

        #ABIDE
        #pheno_dict.get('SubID')
        #['SubID','DxGroup', 'DSMIVTR', 'AgeAtScan', 'Sex', 'Handedness_Category', 'Handedness_Scores', 'FIQ', 'VIQ', 'PIQ', 'IQTest', 'VIQTest', 'PIQTest', ... ,'Age at MPRAGE', 'BMI']+['Site_#', 'Site_Name]

        #discrete labels
        sex = 4
        H = 5
        site = 73
        dx = 1
        #continuous labels
        meanFD = 75
        age = 3
            
        imgNames = [paths[i] for i, y in enumerate(labels) if self.health(y,dx)]
        imgLabels = [y[sex]+self.hand(y,H)+y[site] for y in labels if self.health(y,dx)]

        imgAges = [float(y[age]) for y in labels if self.health(y,dx)]
        imgFD = [float(y[meanFD]) for y in labels if self.health(y,dx)]
        continuous_var = [imgAges,imgFD]
        ## from craddock pyNPAIRS
        # create variables for the basic information
        #maskName = self.inputs.mask_file

        # Read in the mask
        #try:
            #mskImg=nb.load(maskName)
        #except Exception as e:
            #print "Could not load mask %s: %s"%(maskName,e.strerror)

        # find the nonzero indices of the mask
        #mskNdx = np.nonzero(mskImg.get_data())
        maskNdx = np.nonzero(imgNames[0].get_data())

        # initialize array to hold dataset
        dataAry = np.zeros((np.shape(imgNames)[0],np.shape(mskNdx)[1]))

        # now read the image data into the dataset array
        imgCnt=0
        for img in imgNames:
            try:
                imgImg = nb.load(img)
                dataAry[imgCnt,:] = imgImg.get_data()[mskNdx]
                imgCnt = imgCnt + 1
            except Exception as e:
                print "Could not load image %s: %s"%(img,e.message)
                raise
                
        print "Read %d images into %s image array"%(imgCnt,str(np.shape(dataAry)))

        # create the classifier that we intend to use
        svcClassifier = svm.LinearSVC(C=100.0)
        splits = self.splitHalf(imgLabels,10,continuous_var)

        # determine
        nprs=NPAIRS(dataAry, imgLabels,svcClassifier,splits)
        (pred,rep)=nprs.run()
        np.save("prediction_accuracy",pred)
        np.save("reproducibility",rep)
        
        return runtime
        
    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs["pred"] = os.path.abspath('prediction_accuracy')
        outputs["rep"] = os.path.abspath('reproducibility')
        return outputs
