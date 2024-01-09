import joblib
import os

from sklearn.ensemble import RandomForestClassifier

THRESHOLD = 1

Grps = {
    'alcohol':1,
    'carboxylic_acid':2,
    'ketone':2,
    'aldehyde':2,
    'ether':3,
    'ester':3,
    'amino':4,
    'nitro':4,
    'cyano':5,
    'phenyl':6,
    'epoxy':3
}

with open (os.path.join(os.getcwd(), "Xcords-Copy3.job") , "rb") as File :
    columnList = joblib.load(File)

with open (os.path.join(os.getcwd(), "Model2-Copy2.job"), "rb") as modelFile :
    model = joblib.load(modelFile)




def preprocess  (X,Y):
    coor_list = [(k,v) for (k,v) in zip(X,Y)]

    for value in columnList : 
        if value not in X :
            coor_list.append((value,None))
    
    # sorting wrt X coordinate
    coor_list.sort(key = lambda x : x[0])



def pred_FuncGrp (X):
    grp = X
    funcGrp = ""
    for k in Grps.keys():
        if Grps[k] == int(grp):
            funcGrp += f" {k}"  
        pass
    
    if funcGrp != "":
        return funcGrp
    else:
        return "Can't determine the functional group"





def remove_NA (coordinates):
    
    '''
    To remove to the NULL values appearing before the first non-NULL values
    if >= 0.1 : Transmittance
    else : Absorbance   
    '''

    THRESHOLD = 0.1

    for idx , values in enumerate(coordinates)  :
        x,y = values 
        if y is not None :
            set_idx = 0
            if y >= THRESHOLD:
                is_transmitance = True
            else:
                is_transmitance = False 
            
        while set_idx < idx :
            coordinates[idx][1] =  int (is_transmitance)
            set_idx+=1
        break
    
    '''
    To remove the NULL values between two non-NULL values, we will use Linear Interpolation
    Linear Interpolation - just making a line from two non-NULL values to get values for NULL values
    -> Not Writing interpolation from scratch 
    using Pandas.interpolate() 
    '''

    '''
    To remove the NULL values at the end 
    while using Pandas.interpolate(), the NULL values at the end are replaced by the last non-NULL value doesnt matter whether its interpolated or not
    '''


    # updated_df = df[coloumns[n_nonNum:len(coloumns)]].interpolate(method="linear", axis=1)

    # return pd.concat( [ df[coloumns[:n_nonNum]], updated_df, df["is_transmittance"] ], axis = 1)