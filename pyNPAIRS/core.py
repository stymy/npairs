import numpy as np

class NPAIRS(object):
    
    # attributes
    dataAry = None
    dataLbls = None
    classMethod = None
    splitMethod = None
    
    def __init__(self, dataArray=None, dataLabels=None, classifierMethod=None, splits=None  ):
 
        # make sure that we received parameters
        if dataArray is None or dataLabels is None or classifierMethod is None or splits is None:
            print "NPAIRS requires a data array and data labels"
            raise SyntaxError("Missing Parameters")
            
        # make sure that the size of the dataArray, 
        # the size of the dataLabels, and the size
        # of the splits array are  consistent
        if np.shape(dataArray)[0] != np.shape(dataLabels)[0] or np.shape(splits)[1] != np.shape(dataLabels)[0]:
            print "Number of columns in data array (%d), number of labels (%d) and number of indices in split (%d) are not consistent"\
                %(np.shape(dataArray)[0],np.shape(dataLabels)[0],np.shape(splits)[1])
            raise SyntaxError("size of data array does not match labels")
        
        # make classifier is a classifier method
        if not hasattr(classifierMethod,'fit') or not hasattr(classifierMethod,'predict'):
            print "classifier method does not have correct attributes, is it a sklearn classifier?"
            raise SyntaxError("improper classifier")
            
        # assign the attributes
        self.dataAry = dataArray
        self.dataLbls = np.array(dataLabels)
        self.classMethod = classifierMethod
        self.splits = splits
        
    def run(self):
        
        if self.dataAry is None or self.dataLbls is None:
            print "Class must be configured with data array and data labels before calling run()"
            raise SyntaxError("Not Initialized")
        
        print "running NPAIRS"
        print "Configured with %s data array and %s labels"%(str(np.shape(self.dataAry)),str(np.shape(self.dataLbls)))
        
        # initialize our output lists
        rep = np.zeros((self.splits.shape[0],1))
        pred = np.zeros((self.splits.shape[0],1))
        
        # counter to help keep track of things
        cnt = 0
        # iterate over the splits, calculating the NPAIRs metrics
        for split in self.splits:
            
            # first we train on the left half 
            leftCLF = self.classMethod.fit(self.dataAry[split==1,:],self.dataLbls[split==1])
            
            # next calculate the prediction accuracy on the right half
            leftPA = self.classMethod.score(self.dataAry[split==2,:],self.dataLbls[split==2])
            
            # Now swap the roles of the left and right halves and repeat
            rightCLF = self.classMethod.fit(self.dataAry[split==2,:],self.dataLbls[split==2])
            
            # next calculate the prediction accuracy on the right half
            rightPA = self.classMethod.score(self.dataAry[split==1,:],self.dataLbls[split==1])
            
            # average the two prediction accuracies
            pred[cnt] = .5*(rightPA+leftPA)
            
            # now calculate the reproducibility
            rep[cnt] = np.corrcoef(leftCLF.coef_, rightCLF.coef_)[0,1]
            
            print "iter: %d, pred: %3.2f, rep: %3.2f"%(cnt,pred[cnt],rep[cnt])
                        
            # increment the counter
            cnt = cnt+1   

            
        print "finished %d iterations of NPAIRS"%(cnt)
        print "we calculated prediction accuracy %3.2f and reproducibility %3.2f"%(pred.mean(),rep.mean())

        return(pred,rep)
    
    pass


