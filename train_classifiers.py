import nibabel as nb
import numpy as np
from pyNPAIRS.core import NPAIRS
from sklearn import svm
from scipy.stats import ttest_ind
import os

from variables import workingdir
directory = os.path.join(workingdir,'npairs/svc_workflow/_deriv_id_alff_Z_to_standard_smooth/_preproc_id__compcor_ncomponents_5_selector_pc10.linear1.wm0.global1.motion1.quadratic1.gm0.compcor1.csf0/text_files/')
labels=[]
paths=[]
with open(os.path.join(directory,'labels'), 'r') as f:
    for line in f:
        labels.append(line.strip().split(','))
with open(os.path.join(directory,'paths'), 'r') as f:
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
handedness = 5
site = 73
dx = 1
#continuous labels
meanFD = 75
age = 4

#only healthy controls
def health(label):
    boolean = not int(label[dx])==1
    return boolean
#handedness
def hand(label):
    try: handed = str(int(round(float(label[handedness]))))
    except ValueError:
        handed = label[handedness]
    return handed
    
imgNames = [paths[i] for i, y in enumerate(labels) if health(y)]
imgLabels = [y[sex]+hand(y)+y[site] for y in labels if health(y)]

imgAges = [float(y[age]) for y in labels if health(y)]
imgFD = [float(y[meanFD]) for y in labels if health(y)]
continuous_var = [imgAges,imgFD]
## from craddock pyNPAIRS
# create variables for the basic information
maskName = "/home/rschadmin/Data/ADHDworking_dir/tst_mask.nii.gz"

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

# create stratified and controlled splits
def splitHalf(lbls,cnt,contlbls):
    
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

# create the classifier that we intend to use
svcClassifier = svm.LinearSVC(C=100.0)
splits = splitHalf(imgLabels,10,continuous_var)

# determine
nprs=NPAIRS(dataAry, imgLabels,svcClassifier,splits)
(pred,rep)=nprs.run()
