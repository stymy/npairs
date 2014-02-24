import os

workingdir = '/home/rschadmin/Data/ADHDworking_dir'
phenofile = '/home/rschadmin/Data/zarrar_adhd200.csv'
datadir = '/home/rschadmin/Data/ADHD/'

subjects = os.listdir(datadir)[1:]
derivs = ['alff_Z_img','centrality_outputs']
preprocs = ['_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic0.gm0.compcor1.csf0',
'_compcor_ncomponents_5_selector_pc10.linear1.wm1.global1.motion1.quadratic0.gm0.compcor0.csf1']


#phenotype data
pheno_dict = {}
with open(phenofile) as f:
    reader = csv.reader(f,delimiter=",")
    for row in reader:
        pheno_dict[row[0]]=row
