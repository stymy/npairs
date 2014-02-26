import os
import csv
dataset = 'ADHD'

workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
phenodir = '/home/rschadmin/Data/DOCs/'
phenofiles = os.listdir(phenodir)
datadir = '/home/rschadmin/Data/'+dataset

subjects = [s.split('_')[0] for s in os.listdir(datadir)]
exclude_subjects = ['2570769']#[, '2054310', ]
subjects = list(set(subjects) - set(exclude_subjects))

derivs = ['alff','falff']
dg_template = dict(alff=os.path.join('%s*/alff_Z_to_standard_smooth/*/*/*/*/*/*/*/*/*.nii.gz'),\
                  falff=os.path.join('%s*/falff_Z_to_standard_smooth/*/*/*/*/*/*/*/*/*.nii.gz'))
dg_args =     dict(alff=[['subject_id']],\
                  falff=[['subject_id']])
#param files: aimiwat@gelert:/home2/data/Projects/ABIDE_Initiative/CPAC/Output_2013-11-22/pipeline_MerrittIsland/0050020_session_1/power_params/_scan_rest_1_rest/_threshold_0.2/power_params.txt

#phenotype data
#ADHD = 'ScanDir ID'
#ABIDE = 'SubID'
pheno_dict = {}
for phenofile in phenofiles:
    with open(os.path.join(phenodir,phenofile),'rU') as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            pheno_dict[row[0]]=row
        
label_file='/home/rschadmin/Data/'+dataset+'working_dir/label_file'
data_paths='/home/rschadmin/Data/'+dataset+'working_dir/data_paths'
