import os
import csv
import glob
import numpy as np
from collections import defaultdict

dataset = 'NIAK'

#workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
workingdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_workingdir_dparsf'
#datadir = '/home/rschadmin/Data/'+dataset
datadir = '/home2/data/Projects/ABIDE_Initiative/DPARSF/ReNormalize'

dg_template = dict(dr_files= os.path.join(datadir,'*%s/dual_regression/*%s*dmn.nii.gz'),
                   reho_files= os.path.join(datadir,'*%s/reho/*%s*.nii'),
                   falff_files=os.path.join(datadir,'*%s/falff/*%s*.nii'))

dg_args = dict(falff_files= [['preproc_id','subject_id']],
                                            reho_files= [['preproc_id','subject_id']],
                                            dr_files= [['preproc_id','subject_id']])
                                            
#outputdir = '/home/rschadmin/Data/ABIDE_SVC_output'
outputdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_output_dparsf'

subjects =  list(np.load('/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/abideSubjects_HC_12-19_mFD2_reviZed.npy'))
scans = ['1']
#ABIDE
preprocs = ['Results_filt_globalW','Results_filt_noglobalW','Results_nofilt_globalW','Results_nofilt_noglobalW']
