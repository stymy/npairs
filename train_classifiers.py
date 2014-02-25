import nibabel as nb
from sklearn.svm import SVC
from variables import label_file, data_paths
labels=[]
paths=[]
with open(label_file, 'r') as f:
    for line in f:
        labels.append(line.strip().split(','))
with open(data_paths, 'r') as f:
    for line in f:
        paths=[line.strip() for line in f]

#pheno_dict.get('ScanDir ID')
#['ScanDir ID', 'Site', 'Gender', 'Age', 'Handedness', 'DX', 'Secondary Dx ', 'ADHD Measure', 'ADHD Index', 'Inattentive', 'Hyper/Impulsive', 'IQ Measure', 'Verbal IQ', 'Performance IQ', 'Full2 IQ', 'Full4 IQ', 'Med Status', 'QC_Rest_1', 'QC_Rest_2', 'QC_Rest_3', 'QC_Rest_4', 'QC_Anatomical_1', 'QC_Anatomical_2']

phenotype = 2 #sex/gender
svc = SVC()
X = [nb.load(x).get_data() for x in paths]
Y = [float(y[phenotype]) for y in labels]
svc.fit(X,y)
