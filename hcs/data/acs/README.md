# American Community Survey

## About the data

The American Community Survey (ACS), conducted by the U.S. Census Bureau, collects detailed information on American households. 
These data include information on employment and income, demographic information, and, crucially, educational attainment. 
Specifically, beginning in 2009, the ACS began recording up to two undergraduate fields of study for household members.
This has allowed papers such as [Sloane, Hurst, and Black (2019)](https://www.nber.org/papers/w26348) to examine the dynamics of human capital specialization decisions across cohorts. 
For detailed information on using ACS data, [Ruggles et al. (2020)](https://doi.org/10.18128/D010.V10.0).

## Using this directory

In order for this code to be run locally,  the path to raw ACS data in `data/acs/make_acs_df.py needs to be updated. 

Note: this area is under development. 

### Directory structure

Project tree: (all elements under development)
- make_acs_df.py: save extract of ACS dataframe as HDF5 store
- acs_majors.py: creates list of ACS majors 
- acs.h5: HDF5 store, created in `make_acs_df.py`