import os
import csv
import glob
import numpy as np
from collections import defaultdict

dataset = 'NIAK'

#workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
workingdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_workingdir_niak'
#datadir = '/home/rschadmin/Data/'+dataset
datadir = '/home2/data/Projects/ABIDE_Initiative/Derivatives/NIAK/Output'

dg_template = dict(dr_files= os.path.join(datadir,'%s/*%s*_session_%s/dr_tempreg_maps_z_stack/*/*/_spatial_map_PNAS_Smith09_rsn10/*/*/*z_0003_resampled.nii.gz'),
                                            reho_files= os.path.join(datadir,'%s/*%s*_session_%s/reho_Z_img/*/*/*_resampled.nii.gz'),
                                            falff_files=os.path.join(datadir,'%s/*%s*_session_%s/falff_Z_img/*/*/*hp*/*lp*/*_resampled.nii.gz'))

dg_args = dict(falff_files= [['preproc_id','subject_id', 'scan_id']],
                                            reho_files= [['preproc_id','subject_id', 'scan_id']],
                                            dr_files= [['preproc_id','subject_id', 'scan_id']])
                                            
#outputdir = '/home/rschadmin/Data/ABIDE_SVC_output'
outputdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_output_niak'

subjects =  list(np.load('/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/abideSubjects_HC_12-19_mFD2_reviZed.npy'))
scans = ['1']
#ABIDE
preprocs = ['pipeline_filt_global','pipeline_filt_noglobal','pipeline_nofilt_global','pipeline_nofilt_noglobal']
