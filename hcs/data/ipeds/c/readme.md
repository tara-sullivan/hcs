# IPEDS Completion Surveys

## About the data

Integrated Postsecondary Education Data System (IPEDS) data are collected annually by the National Center for Educational Statistics (NCES) and describe the universe of institutions that participate in federal student financial aid programs. 
IPEDS Completion Surveys describe all degrees and certificates awarded at postsecondary institutions by field of study, gender, and race.
For more details on the IPEDS series, please visit https://nces.ed.gov/ipeds/.

## Using this directory

In order for this code to be run locally, the path to raw IPEDs completion surveys in `data/ipeds/c/clean_data/ipeds_cip_merge.do` and `data/ipeds/c/clean_data/ipeds_c_clean.do` needs to be updated.

### Directory structure

Project tree: 
- clean_data/
    - ipeds_c_clean.do: creates cip2names.dta, cip4names.dta [ignored in .gitignore]
    - ipeds_cip_merge.do: creates ipeds_c_all.dta [ignored in .gitignore]
    - make_df.py
    - historical_data/
        * historical_df.py
        * table28/
            * table28.pdf
            * table28b.zip
            * table28a-page-1-table-1.csv 
            * table28c-page-1-table-1.csv
            * table28a.pdf 
            * table28c.pdf
            * table28a.zip 
            * table28c.zip
- plot_by_n.py
- plot_by_cip.py
- ipeds_plots.py
- save_ipeds_plots.py


## Cleaning IPEDS completion data

Raw data can be found here: https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx

CIP codes are used to identify fields of study in IPEDS data.
These codes change over time, and these changes need to be accounted for in order to make a consistent time series.
The NCES provides crosswalk between different versions of CIP codes, but these are not straightforward to use.
The program `ipeds_cip_merge.do` creates a concordance between different versions of CIP codes. 
It creates many temporary files that will be used by `ipeds_c_clean.do`, but also creates two files that will be used to create dictionaries in python: `cip2names.dta` and `cip4names.dta`.

The program `ipeds_c_clean.do` cleans raw IPEDS data files and creates a time series. 
It uses the raw data from the IPEDS website and the temporary files created by `ipeds_cip_merge.do` to create a file `ipeds_c_all.dta`, all of which will be saved in the `clean_data` sub-folder (note data files are ignored due to size).
Note that it's possible to run this program to produce only a cross section of data for a particular year; see the program for details.

The program `make_df.py` reads the smaller dataset `ipeds_c_all.dta` and creates a dataframe from the appropriate observations. It also creates dictionaries from `cip2names.dta` and `cip4names.dta`.

The subfolder historical_data.py creates a longer time series than is available through IPEDS. 
I downloaded "120 Years of American Education" from NCES website: (https://nces.ed.gov/pubsearch/pubsinfo.asp?pubid=93442).
I saved table 28 as a pdf, and used excalibur-py to save the data from each of the three pages as a csv.
These data are turned into a compatible dataframe in historical_data.py

Note that I wrote two key cleaning programs in Stata before navigating to python, hence the change in language. 

## Making IPEDS completion survey plots

All IPEDS plots used in this project are created in `ipeds_plots.py`. This program calls `plot_by_n.py`, which plots the total number of degrees completed by men and by women. It also callls `plot_by_cip.py`, which plots the total number of degrees completed by field of study (or lists of fields of study). 
The program `plot_by_cip.py` allows you to create ratio plots or area plots, and saves the plots in a way that works for beamer presentations or for tex articles. As such, some code that saves graphs in helpful ways is in `save_ipeds_plots.py`. 
