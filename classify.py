from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec, InputMultiPath
import nibabel as nb
import numpy as np
from pyNPAIRS.core import NPAIRS
from sklearn import svm
from scipy.stats import ttest_ind
import os
from nipype.utils.filemanip import split_filename

class ClassifyInputSpec(BaseInterfaceInputSpec):
    label_file = traits.File(exists=True, desc="labels")
    path_file = traits.File(exists=True, desc="paths")
    mask_file = traits.File(exists=True, desc="brain_mask")

class ClassifyOutputSpec(TraitedSpec):
    pred = traits.File(desc="prediction accuracy")
    rep = traits.File(desc="reproducibility")
    imgs = traits.File(desc="img labels")
    splits = traits.File(desc="splits")
    sexs = traits.File(desc="sex labels")
    coefs = traits.File(desc='CLF coeffs')
    datary = traits.File(desc='data array for CLF')

class Classify(BaseInterface):
    input_spec = ClassifyInputSpec
    output_spec = ClassifyOutputSpec
    
    def health(self,label,dx):
        boolean = not int(label[dx])==1
        return boolean

    def hand(self,label,H):
        handed = label[H]
        if label[H] == 'R':
            handed = str(1)
        if label[H] == 'L':
            handed = str(2)
        if label[H] == '':
            try: handed = str(int(round(float(label[H+1])/100)))
            except ValueError:
                print handed
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
            ulbls = np.unique([m[-2:] for m in lbls]) #unique labels without gender
            eqlbls = [m[-2:] for m in lbls]
            for lbl in ulbls:
                #separate male and female so we can equalize gender btwn splits
                #lbls_Fem = [n[-2:] for n in lbls if n.startswith('2')]               
                #lbls_Mal = [n[-2:] for n in lbls if n.startswith('1')]
                #alllbls = [i for i,x in enumerate(lbls) if x.endswith(lbl)]
                # get the indices of the label
                #lNdx_Fem = [i for i,x in enumerate(lbls_Fem) if x.endswith(lbl)]
                #lNdx_Mal = [i for i,x in enumerate(lbls_Mal) if x.endswith(lbl)]
                lNdx = [i for i,x in enumerate(lbls) if x.endswith(lbl)]
                
                #find smaller sample
                #if len(lNdx_Fem)<len(lNdx_Mal):
                #    lNdx_Mal = np.random.choice(lNdx_Mal,size=len(lNdx_Fem),replace=False)
                #if len(lNdx_Fem)>len(lNdx_Mal):
                #    lNdex_Fem = np.random.choice(lNdx_Fem,size=len(lNdx_Mal),replace=False)
                # determine half of the number of the labels
                #numL2 = int(round(len(lNdx_Fem)/2.0))
                numL2 = int(round(eqlbls.count(lbl)/2.0))
                #import pdb; pdb.set_trace()
                
                lHalf = np.random.choice(lNdx,size=numL2,replace=False)
                tmp_splits[lHalf]=2
                #if not list(lNdx_Fem)==[] and not list(lNdx_Mal)==[]: #check if no indices are lbl
                 #   lHalf_Fem = np.random.choice(lNdx_Fem,size=numL2/2,replace=False)
                  #  lHalf_Mal = np.random.choice(lNdx_Mal,size=numL2/2,replace=False)
                
                   # tmp_splits[lHalf_Fem]=2
                    #tmp_splits[lHalf_Mal]=2
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

        return splits, ulbls
                
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

        #index of discrete labels
        sex = 4
        H = 5
        site = 10
        dx = 1
        #index fo continuous labels
        meanFD = 12
        age = 3
        
        #imgSex = [y[sex] for y in labels if self.health(y,dx) and len(self.hand(y,H))==1]
          
        imgNames_F = [paths[i] for i, y in enumerate(labels) if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '2']
        imgNames_M = [paths[i] for i, y in enumerate(labels) if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '1']
        imgNames = imgNames_F+imgNames_M[:len(imgNames_F)]
        
        imgLabels_F = [y[sex]+self.hand(y,H)+y[site] for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '2']
        imgLabels_M = [y[sex]+self.hand(y,H)+y[site] for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '1']
        imgLabels = imgLabels_F+imgLabels_M[:len(imgLabels_F)]

        imgSex_F = [y[sex] for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '2']
        imgSex_M = [y[sex]) for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '1']
        imgSex = imgSex_F+imgSex_M[:len(imgSex_F)]
        
        imgAges_F = [float(y[age]) for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '2']
        imgAges_M = [float(y[age]) for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '1']
        imgAges = imgAges_F+imgAges_M[:len(imgAges_F)]
        
        imgFD_F = [float(y[meanFD]) for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '2']
        imgFD_M = [float(y[meanFD]) for y in labels if self.health(y,dx) and len(self.hand(y,H))==1 and y[sex] == '1']
        imgFD = imgFD_F+imgFD_M[:len(imgFD_F)]
        
        continuous_var = [imgAges,imgFD]
        
        ## from craddock pyNPAIRS
        # create variables for the basic information
        maskName = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/rois/mask_100percent.nii.gz'

        # Read in the mask
        try:
            mskImg=nb.load(maskName)
        except Exception as e:
            print "Could not load mask %s: %s"%(maskName,e.strerror)

        # find the nonzero indices of the mask
        mskNdx = np.nonzero(mskImg.get_data())

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
        svcClassifier = svm.LinearSVC(C=0.000000001)
        
        _, base, _ = split_filename(self.inputs.path_file[0])
        
        np.save(os.path.abspath(base+"img_labels.npy"),imgLabels)
        #np.save(os.path.abspath(base+"sex_labels.npy"),imgSex)
        np.save(os.path.abspath(base+"data_array.npy"),dataAry)
        
        splits, ulbls = self.splitHalf(imgLabels,100,continuous_var)
        
        np.save(os.path.abspath(base+"splits.npy"),splits)
        # determine
        nprs=NPAIRS(dataAry, imgSex, svcClassifier,splits)
        (pred,rep,leftcoefs,rightcoefs)=nprs.run()
        coefs = [leftcoefs,rightcoefs]

        np.save(os.path.abspath(base+"prediction_accuracy.npy"),pred)
        np.save(os.path.abspath(base+"reproducibility.npy"),rep)
        np.save(os.path.abspath(base+"coefs.npy"),coefs)

        return runtime
        
    def _list_outputs(self):
        outputs = self._outputs().get()
        _, base, _ = split_filename(self.inputs.path_file[0])
        outputs["pred"] = os.path.abspath(base+'prediction_accuracy.npy')
        outputs["rep"] = os.path.abspath(base+'reproducibility.npy')
        outputs["imgs"] = os.path.abspath(base+'img_labels.npy')
        outputs["splits"] = os.path.abspath(base+'splits.npy')
        outputs["sexs"] = os.path.abspath(base+'sex_labels.npy')
        outputs["coefs"] = os.path.abspath(base+'coefs.npy')
        outputs["datary"] = os.path.abspath(base+"data_array.npy")
        return outputs
