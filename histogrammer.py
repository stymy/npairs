import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

import numpy as np
from variables import pheno_dict, meta_subs
from collections import defaultdict

#discrete labels
sex = 4
H = 5
site = 73
site_name = 74
dx = 1
#continuous labels
meanFD = 75
age = 3

phenostats = defaultdict(list)
for subject in meta_subs:
    print subject
    phenostats[pheno_dict.get(subject)[site_name].rstrip('.csv')].append(float(pheno_dict.get(subject)[age]))

agebins = np.linspace(0,40,40)   

for x in phenostats.viewkeys():
    print phenostats[x]
    plt.hist(phenostats[x], agebins, alpha=0.3, label=x)

#plt.show()
plt.legend(loc='upper right',fontsize='xx-small')
plt.savefig('/home2/aimiwat/histogram.png')
