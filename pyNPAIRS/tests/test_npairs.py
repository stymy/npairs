'''
Created on Feb 24, 2014

@author: cameron
'''
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testNPAIRS(self):
        from pyNPAIRS.core import NPAIRS
        import nibabel as nb
        import numpy as np
        import os
        from sklearn import svm
        
        print os.getcwd()
        
        # create variables for the basic information
        maskName = "tst_mask.nii.gz"
        imgNames = ["tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_F.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz",
                    "tst_img_M.nii.gz"
                    ] 
        
        imgLabels = ['F','F','F','F','F','F','F','F','F','F',\
                     'M','M','M','M','M','M','M','M','M','M']
        
        
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
                print "Could not load image %s: %s"%(img,e.strerror)
                raise
                
        print "Read %d images into %s image array"%(imgCnt,str(np.shape(dataAry)))
        
        # create a basic splitter method
        def splitHalf(lbls,cnt):
            
            # first we initialize our split 
            splits=np.ones((cnt,len(lbls)))
            
            for lbl in np.unique(lbls):
                
                # get the indices of the label
                lNdx = [i for i,x in enumerate(lbls) if x == lbl]
                
                # determine half of the number of the labels
                numL2 = int(round(lbls.count(lbl)/2))
                
                # randomly generate cnt splits
                for c in range(0,cnt):
                    lHalf = np.random.choice(lNdx,size=numL2,replace=False)
                    splits[c,lHalf]=2
                
            return splits
                
           
        # psuedo for stratified and controlled splits
        # create a basic splitter method
       # def splitHalf(lbls,cnt):
            
            # first we initialize our split 
           # splits=np.ones((cnt,len(lbls)))
   
            # randomly generate cnt splits
           # c = 0
           # while c < cnt:
                
                             
                #for lbl in np.unique(lbls):
                
                    # get the indices of the label
                #    lNdx = [i for i,x in enumerate(lbls) if x == lbl]
                
                    # determine half of the number of the labels
                #    numL2 = int(round(lbls.count(lbl)/2))
                
                #    lHalf = np.random.choice(lNdx,size=numL2,replace=False)
                #    splits[c,lHalf]=2

                # calculate ttest for each of the continuous varaibles you would like to control for
                
               # if all of the control variables are insignificant p > 0.5 and haven't previously generated that split:
                #    c=c+1
                 
                
        #    return splits
        
        # create the classifier that we intend to use
        svcClassifier = svm.LinearSVC(C=100.0)
        splits = splitHalf(imgLabels,10)
        
        # determine
        nprs=NPAIRS(dataAry, imgLabels,svcClassifier,splits)
        (pred,rep)=nprs.run()
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()