import os
import csv

workingdir = '/home/rschadmin/Data/ADHDworking_dir'
phenofile = '/home/rschadmin/Data/zarrar_adhd200.csv'
datadir = '/home/rschadmin/Data/ADHD/'

#subjects = os.listdir(datadir)
subjects = ['2081754_','2104012_',]
derivs = ['centrality_outputs'] #'alff_Z_img',
preprocs = ['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic0.gm0.compcor1.csf0',
'_compcor_ncomponents_5_selector_pc10.linear1.wm1.global1.motion1.quadratic0.gm0.compcor0.csf1']

#phenotype data
pheno_dict = {}
with open(phenofile) as f:
    reader = csv.reader(f,delimiter=",")
    for row in reader:
        pheno_dict[row[0]]=row
        
label_file='/home/rschadmin/Data/ADHDworking_dir/label_file'
data_paths='/home/rschadmin/Data/ADHDworking_dir/data_paths'
