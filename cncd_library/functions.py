import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
def checkPhenoCode(dataframe,phenotype): 
    """ 

    This function checks disprencies in dataframes using phenotype files

    Parameters:
    dataframe (pandas dataframe): dataframe to be checked

    phenotype (pandas dataframe): phenotype file


    """ 
    phenotype['status'] = 0
    phenotype.loc[phenotype["disease_status"].str.contains("CASE"), "status"] = 1
    phenotype.loc[phenotype["disease_status"].str.contains("CONTROL"), "status"] = 0
    phenotype.loc[phenotype["disease_status"].str.contains("CASE/CONTROL"), "status"] = np.nan
    phenotype.dropna(how='all',subset=['status'],inplace=True)

    incorrect_phenotypes = (dataframe.merge(phenotype, on=['center_alpha','status'], how='left', indicator=True)
        .query('_merge == "left_only"')
        .drop('_merge', 1))
    incorrect_phenotypes = incorrect_phenotypes[['study_id','status','center_alpha']].copy()
    df = pd.merge(incorrect_phenotypes,phenotype,how='inner',on=['center_alpha'],suffixes=('', '_correct'))
    return(df[['study_id','status','center_alpha','disease_status','status_correct']])
import pandas as pd
import numpy as np



def checkGender(dataframe,check = ''):
    """
    Checks gender and age with name and bound values


    Parameters:
    dataframe (pandas dataframe): dataframe to be checked

    check (string): check the gender of the dataframes

    returns dataframe (pandas dataframe)

    """

    Returns:
    global gender_data,condition_male,condition_female
    if 'first_name' in list(dataframe.columns):
        bucket_gender_check = ['BIBI', 'MRS','BANO','W/O','D/O','MISS','MS','BB','S/O']
        gender_data = dataframe[['study_id','first_name','gender','age']].copy()
        gender_data['result'] = gender_data['first_name'].apply(lambda x : ','.join([item for item in str(x).split() if item.upper() in bucket_gender_check]))
    else:
        bucket_gender_check = ['BIBI', 'MRS','BANO','W/O','D/O','MISS','MS','BB','S/O']
        gender_data = dataframe[['study_id','name','gender','age']].copy()
        gender_data['result'] = gender_data['name'].apply(lambda x : ','.join([item for item in str(x).split() if item.upper() in bucket_gender_check])) 

    condition_male = (gender_data['result'] == 'S/O') & (gender_data['gender'] == 2) | (gender_data['age'] > 105) | (gender_data['age'] < 16)
    condition_female = (gender_data['result'].isin(bucket_gender_check[:-1]) ) & (gender_data['gender'] == 1) | (gender_data['age'] > 105) | (gender_data['age'] < 16)
    
    if check == 'male':
        check_male = gender_data[condition_male]
        check_male.dropna(inplace=True)
        return(check_male)
    elif check == 'female':
        check_female = gender_data[condition_female]
        check_female.dropna(inplace=True)
        return(check_female)
    else:
        print('Enter Correct Gender')