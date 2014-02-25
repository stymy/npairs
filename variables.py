import os
import csv
dataset = 'ADHD'

workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
phenodir = '/home/rschadmin/Data/DOCs/'
phenofiles = os.listdir(phenodir)
datadir = '/home/rschadmin/Data/'+dataset

subjects = [s.split('_')[0] for s in os.listdir(datadir)]
derivs = ['alff_Z_img','falff_Z_img']
preprocs = \
['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic0.gm0.compcor1.csf0',
'_compcor_ncomponents_5_selector_pc10.linear1.wm1.global1.motion1.quadratic0.gm0.compcor0.csf1']
#['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic0.gm0.compcor1.csf0']


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
