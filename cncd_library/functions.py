import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
def checkPhenoCode(dataframe,phenotype): 
    """ 

    This function checks disprencies in dataframes using phenotype files

    Parameters:
    dataframe (pandas dataframe): dataframe to be checked

    phenotype (pandas dataframe): take phenotype coding list from googlesheet


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

#========================================================== Check Gender ====================================================
def checkGender(dataframe,check = ''):
    """
    Checks gender and age with name and bound values


    Parameters:
    dataframe (pandas dataframe): dataframe to be checked

    check (string): check the gender of the dataframes

    returns dataframe (pandas dataframe)

    """
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

def dm_qc_status(dataframe):
    """
    This function checks DM Diabetes status disprencies in dataframes using phenotype files

    Parameters:
    dataframe (pandas dataframe): dataframe to be checked


    """
    status = dataframe.query('(dm == 1 & status != 1) | (dm == 0 & status != 0) | (dm_medicine == 1 & status != 1) ')[['study_id','status','dm','dmage','dm_medicine']].copy()
    return(status)


def nafld_qc_status(dataframe):
        """
    This function checks NAFLD Fatty Liver Diesease status disprencies in dataframes using phenotype files

    Parameters:
    dataframe (pandas dataframe): dataframe to be checked


    """
    status = dataframe.query('((status == 1 & (fibroscan_capscore_mean.isnull() & ultrasound_report.isnull())) | (status == 1 & diagnosed_fatty_liver_disease != 1) | (status == 0 & fibroscan_capscore_mean.notnull()) | (status == 0 & ultrasound_report.notnull()) | (status == 0 & (diagnosed_fatty_liver_disease != 0)))')[['study_id','status','fibroscan_capscore_mean','ultrasound_report','diagnosed_fatty_liver_disease']]
    return(status)


def nafld_check_women_history(dataframe):

    """
    This function checks NAFLD Women History disprencies in dataframes using phenotype files

    Parameters:
    dataframe (pandas dataframe): dataframe to be checked

    

    """

    nafld_wh_columns = ['study_id','name','gender','age','status','subject_menstrual_state','subject_mensturation_last_12_months','subject_age_stop_mensturation','subject_reason_stop_menstruation','use_hormone_replacement_therapy','htn_pregnancy','dm_pregnancy','premature_birth']
    male_with_fh = dataframe[dataframe['gender'] == 1].query('subject_menstrual_state > 0 or subject_mensturation_last_12_months > 0 or subject_age_stop_mensturation > 0 or subject_reason_stop_menstruation > 0 or use_hormone_replacement_therapy > 0 or htn_pregnancy > 0 or dm_pregnancy > 0 or premature_birth > 0')
    
    return(male_with_fh[nafld_wh_columns])