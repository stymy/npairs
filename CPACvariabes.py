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

#phenodir = '/home/rschadmin/Data/DOCs/'
phenodir = '/home2/data/Originals/ABIDE/Docs/Phenotypics_motion_scannerProtocols/PhenotypicDataForConsortiumUse/'
phenofiles = os.listdir(phenodir)
#motiondir = '/home2/data/Projets/ABIDE_Initiative'
motiondir = '/home2/data/Projects/ABIDE_Initiative/CPAC/Output_2013-11-22/pipeline_MerrittIsland'

motionfiles = glob.glob(os.path.join(motiondir+'/*/power_params/_scan_rest_1_rest/_threshold_0.2/*'))

subjects =  list(np.load('/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/abideSubjects_HC_12-19_mFD2_reviZed.npy'))
scans = ['1']

pipelines = ['pipeline_RameyBorough','pipeline_MerrittIsland']

#ABIDE
preprocs = ['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0',
'_compcor_ncomponents_5_selector_pc10.linear1.wm0.global1.motion1.quadratic1.gm0.compcor1.csf0']

#phenotype data
#ADHD = 'ScanDir ID'
#ABIDE = 'SubID'
phenotyped_subs = set()
motiontyped_subs = set()
pheno_dict = defaultdict(list)
for i, phenofile in enumerate(phenofiles):
    with open(os.path.join(phenodir,phenofile),'rU') as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            pheno_dict[row[0]]=row
            if phenofile == 'UM1_P2FRV.csv':#'Leuven2_P1.5.csv'
                pheno_dict[row[0]].append('')
                pheno_dict[row[0]].append('')
            #if phenofile == 'Leuven2_P1.5.csv':
                #pheno_dict[row[0]].append('')
            pheno_dict[row[0]].append(str(i))
            pheno_dict[row[0]].append(phenofile)
	    phenotyped_subs.add(str(row[0]))

for motionfile in motionfiles:
    with open(motionfile,'rU') as f:
        reader = csv.reader(f,delimiter=",")
        pheno_dict['Subject'] = reader.next()
        for row in reader:
            subject = row[0].split('_')[0].lstrip('0') #subject_id
            pheno_dict[subject].append(row[2])
            motiontyped_subs.add(str(subject))

meta_subs = phenotyped_subs & motiontyped_subs
