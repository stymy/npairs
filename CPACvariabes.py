import os
import csv
import glob
import numpy as np
from collections import defaultdict

dataset = 'CPAC'

#workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
workingdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_workingdir_cpac'
#datadir = '/home/rschadmin/Data/'+dataset
datadir = '/home2/data/Projects/ABIDE_Initiative/CPAC/Output_2013-11-22/'

dg_template = dict(dr_files= os.path.join(datadir,'%s/*%s*/dr_tempreg_maps_z_stack_to_standard/_scan_rest_%s_rest/*/*/*/%s/*/*.nii.gz'),
                                            reho_files= os.path.join(datadir,'%s/*%s*/reho_Z_to_standard_smooth/_scan_rest_%s_rest/*/*/*/%s/*/*.nii.gz'),
                                            falff_files=os.path.join(datadir,'%s/*%s*/falff_Z_to_standard_smooth/_scan_rest_%s_rest/*/*/*/%s/*/*/*/*.nii.gz'),
                                            mask_file = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/rois/mask_100percent.nii.gz')

dg_args = dict(falff_files= [['pipeline_id','subject_id', 'scan_id','preproc_id']],
                                            reho_files= [['pipeline_id','subject_id', 'scan_id','preproc_id']],
                                            dr_files= [['pipeline_id','subject_id', 'scan_id','preproc_id']],
                                            mask_file= [['pipeline_id','subject_id','scan_id']])

#outputdir = '/home/rschadmin/Data/ABIDE_SVC_output'
outputdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_output_cpac'

subjects =  list(np.load('/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/abideSubjects_HC_12-19_mFD2_reviZed.npy'))
scans = ['1']

pipelines = ['pipeline_RameyBorough','pipeline_MerrittIsland']

#ABIDE
preprocs = ['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0',
'_compcor_ncomponents_5_selector_pc10.linear1.wm0.global1.motion1.quadratic1.gm0.compcor1.csf0']