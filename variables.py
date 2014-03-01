import os
import csv
import glob
import numpy as np
from collections import defaultdict

dataset = 'vars'

#workingdir = '/home/rschadmin/Data/'+dataset+'working_dir'
workingdir = '/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/SVC_workingdir'
#datadir = '/home/rschadmin/Data/'+dataset
datadir = '/home2/data/Projects/ABIDE_Initiative/CPAC/Output_2013-11-22/pipeline_MerrittIsland/'
#derivdir = datadir+'_DERIV/'

#phenodir = '/home/rschadmin/Data/DOCs/'
phenodir = '/home2/data/Originals/ABIDE/Docs/Phenotypics_motion_scannerProtocols/PhenotypicDataForConsortiumUse/'
phenofiles = os.listdir(phenodir)
#motiondir = '/home2/data/Projets/ABIDE_Initiative'
motiondir = '/home2/data/Projects/ABIDE_Initiative/CPAC/Output_2013-11-22/pipeline_MerrittIsland'

motionfiles = glob.glob(os.path.join(motiondir+'/*/power_params/_scan_rest_1_rest/_threshold_0.2/*'))

subjects =  list(np.load('/data/Projects/ABIDE_Initiative/CPAC/abide/for_grant/zarrar_abide_sublist.npy'))

phenotyped_subs = set()
motiontyped_subs = set()
pheno_dict = defaultdict(list)
for i, phenofile in enumerate(phenofiles):
    with open(os.path.join(phenodir,phenofile),'rU') as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            pheno_dict[row[0]]=row
            #if phenofile == 'UM1_P2FRV.csv':#'Leuven2_P1.5.csv'
                #pheno_dict[row[0]].append('')
                #pheno_dict[row[0]].append('')
            #if phenofile == 'Leuven2_P1.5.csv':
                #pheno_dict[row[0]].append('')
            pheno_dict[row[0]].insert(10,str(i))
            pheno_dict[row[0]].insert(11,phenofile)
	    phenotyped_subs.add(str(row[0]))

for motionfile in motionfiles:
    with open(motionfile,'rU') as f:
        reader = csv.reader(f,delimiter=",")
        pheno_dict['Subject'] = reader.next()
        for row in reader:
            subject = row[0].split('_')[0].lstrip('0') #subject_id
            pheno_dict[subject].insert(12,row[2])
            motiontyped_subs.add(str(subject))

meta_subs = phenotyped_subs & motiontyped_subs
