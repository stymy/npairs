import os
import csv
import glob

dataset = 'ABIDE'

workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
datadir = '/home/rschadmin/Data/'+dataset
derivdir = datadir+'_DERIV/'
outputdir = '/home/rschadmin/Data/ABIDE_SVC_output'

phenodir = '/home/rschadmin/Data/DOCs/'
phenofiles = os.listdir(phenodir)
motionfiles = glob.glob(os.path.join(datadir+'/*/power_params/_scan_rest_1_rest/_threshold_0.2/*'))

subjects = [s.split('_')[0] for s in os.listdir(datadir)]
subjects_eign = [s.split('_')[0] for s in os.listdir(os.path.join(derivdir,'Eigen'))]
subjects_cent = [s.split('_')[0] for s in os.listdir(os.path.join(derivdir,'Cent'))]
#exclude_subjects = ['2570769'] ADHD
exclude_subjects = ['0050058'] #ABIDE
subjects = list(set(subjects)&set(subjects_eign)&set(subjects_cent) - set(exclude_subjects))
methods = ['alff_Z_to_standard_smooth','falff_Z_to_standard_smooth']
derivs = ['Cent','Eigen']
deriv_types = ['binarize','weighted']
#ADHD preprocs =['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic0.gm0.compcor1.csf0',
# '_compcor_ncomponents_5_selector_pc10.linear1.wm1.global1.motion1.quadratic0.gm0.compcor0.csf1']
#ABIDE
preprocs = ['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0',
'_compcor_ncomponents_5_selector_pc10.linear1.wm0.global1.motion1.quadratic1.gm0.compcor1.csf0']

pprocs = ['_scan_nofilt_global','_scan_nofilt_noglobal','_scan_filt_global','_scan_filt_noglobal']

#phenotype data
#ADHD = 'ScanDir ID'
#ABIDE = 'SubID'
pheno_dict = {}
for i, phenofile in enumerate(phenofiles):
    with open(os.path.join(phenodir,phenofile),'rU') as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            pheno_dict[row[0]]=row
            pheno_dict[row[0]].append(str(i))
            pheno_dict[row[0]].append(phenofile)
for motionfile in motionfiles:
    with open(motionfile,'rU') as f:
        reader = csv.reader(f,delimiter=",")
        pheno_dict['Subject'] = reader.next()
        for row in reader:
            subject = row[0].split('_')[0].lstrip('0') #subject_id
            pheno_dict[subject].append(row[2])
