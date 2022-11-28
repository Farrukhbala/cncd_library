class CNCD:


    def checkPhenoCode(self,dataframe,phenotype): 
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