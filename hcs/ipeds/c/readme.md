# IPEDS Completion Surveys

## About the data

Integrated Postsecondary Education Data System (IPEDS) data are collected annually by the National Center for Educational Statistics (NCES) and describe the universe of institutions that participate in federal student financial aid programs. 
IPEDS Completion Surveys describe all degrees and certificates awarded at postsecondary institutions by field of study, gender, and race.
For more details on the IPEDS series, please visit https://nces.ed.gov/ipeds/.

## Using this directory

### Directory structure

Project tree: 
- clean_data
    - ipeds_c_clean.do
    - ipeds_cip_merge.do
    - cip2names.dta
    - cip4names.dta


## Cleaning IPEDS data

Raw data can be found here: https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx

CIP codes are used to identify fields of study in IPEDS data.
These codes change over time, and these changes need to be accounted for in order to make a consistent time series.
The NCES provides crosswalk between different versions of CIP codes, but these are not straightforward to use.
The program `ipeds_cip_merge.do.` creates a concordance between different versions of CIP codes. 
It creates many temporary files that will be used by `ipeds_c_clean.do`, but also creates two files that will be used to create dictionaries in python: `cip2names.dta` and `cip4names.dta`.

The program `ipeds_c_clean.do` cleans raw IPEDS data files and creates a time series. 
It uses the raw data from the IPEDS website and the temporary files created by `ipeds_cip_merge.do`.
Note that it's possible to run this program to produce a cross section of data for a particular year.

Note that I wrote two key cleaning programs in Stata before navigating to python, hence the change in language. 
