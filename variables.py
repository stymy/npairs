import os
import csv
import glob
import numpy as np
from collections import defaultdict

dataset = 'CPAC'

#workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
workingdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_workingdir'
#datadir = '/home/rschadmin/Data/'+dataset
datadir = '/home2/data/Projects/ABIDE_Initiative/CPAC/Output_2013-11-22/pipeline_MerrittIsland/'
#derivdir = datadir+'_DERIV/'
#outputdir = '/home/rschadmin/Data/ABIDE_SVC_output'
outputdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_output'

#phenodir = '/home/rschadmin/Data/DOCs/'
phenodir = '/home2/data/Originals/ABIDE/Docs/Phenotypics_motion_scannerProtocols/PhenotypicDataForConsortiumUse/'
phenofiles = os.listdir(phenodir)
#motiondir = '/home2/data/Projets/ABIDE_Initiative'
motiondir = '/home2/data/Projects/ABIDE_Initiative/CPAC/Output_2013-11-22/pipeline_MerrittIsland'

motionfiles = glob.glob(os.path.join(motiondir+'/*/power_params/_scan_rest_1_rest/_threshold_0.2/*'))

subjects =  list(np.load('/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/abideSubjects_HC_12-19_mFD2_reviZed.npy'))
#subjects = [s.split('_')[0] for s in os.listdir(datadir)]
#subjects_eign = [s.split('_')[0] for s in os.listdir(os.path.join(derivdir,'Eigen'))]
#subjects_cent = [s.split('_')[0] for s in os.listdir(os.path.join(derivdir,'Cent'))]
#exclude_subjects = ['2570769'] ADHD
#exclude_subjects = ['0050058','120702','120705','120707','120708','120709','120710','121339','121340','121341','121346','121347','121348'] #ABIDE
#subjects = list(set(subjects) - set(exclude_subjects))
#methods = ['falff_Z_to_standard_smooth']
#derivs = ['Cent','Eigen']
#deriv_types = ['binarize','weighted']
scans = ['1']
#ADHD preprocs =['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic0.gm0.compcor1.csf0',
# '_compcor_ncomponents_5_selector_pc10.linear1.wm1.global1.motion1.quadratic0.gm0.compcor0.csf1']
#ABIDE
preprocs = ['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0',
'_compcor_ncomponents_5_selector_pc10.linear1.wm0.global1.motion1.quadratic1.gm0.compcor1.csf0']

#pprocs = ['_scan_nofilt_global','_scan_nofilt_noglobal','_scan_filt_global','_scan_filt_noglobal']

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
            if phenofile == 'UM1_P2FRV.csv':
                pheno_dict[row[0]].append('')
                pheno_dict[row[0]].append('')
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
