# cncd_library


cncd_library is a Python package that contains some handy functions that we use on daily basis at CNCD. 


## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cncd_library like below. 
Rerun this command to check for and install  updates .
```bash
pip install git+https://github.com/Farrukhbala/cncd_library
```

## Usage
Features:
* functions.checkPhenoCode  --> generates a new dataframe containing correction of Phenotype Coding list 


#### Demo of some of the features:
```python
data = pd.read_csv(r'file_directory')

#take phenotype coding list from googlesheet
pheno = pd.read_csv(r'phenotype_coding_list.csv')

cncd.checkPhenoCode(data,pheno)

```
