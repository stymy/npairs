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
        
        # create variables for the basic information
        maskName = "tst_mask.nii.gz"
        imgNames = ["tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgF.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz",
                    "tst_imgM.nii.gz"
                    ] 
        
        imgLabels = ['F','F','F','F','F','F','F','F','F','F',\
                     'M','M','M','M','M','M','M','M','M','M']
        
        
        np=NPAIRS()
        np.run()
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()