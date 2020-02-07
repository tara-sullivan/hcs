capture restore
set more off
set type double
clear all

local readdata 0
local cipnames 0

if "`c(os)'" == "MacOSX" {
	cd "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/"
}
else {
	cd "Z:\hcs"
}

*do Z:\hcs\code\ipeds\ipeds_cip_merge.do
*do "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/code/ipeds/ipeds_clean.do"

local datapath "data/ipeds"

/*******************************************************************************
* Missing from concordance

Here I check which CIP codes are missing from the concordances. 
There are three concordances:
A. 1985 to 1990
B. 1990 to 2000
C. 2000 to 2010

I also have lists of the CIP codes from the dictionaries here:
https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx

*******************************************************************************/

***************************
* Problems in concordance *
***************************

foreach yr of numlist 1987 1990 {
if `yr' == 1987 {
	local startyr = 1985
	local endyr = 1990
	local crosswalk "Crosswalk_CIP85toCIP90"
	local var_cipstart "CIP85"
	local var_cipend "CIP90"
	local var_titlestart "CIPTITLE85"
	local var_titleend "CIPTITLE90"
}
if `yr' == 1990 {
	local startyr = 1990
	local endyr = 2000
	local crosswalk "Crosswalk_CIP90toCIP2K"
	local var_cipstart "CIPCODE90"
	local var_cipend "CIPCODE2k"
	local var_titlestart "CIPTEXT90"
	local var_titleend "CIPTEXT2K"
}

di "********"
di "* `yr' *"
di "********"
********
* 1990 *
**********************************
* A. Make basic edits to crosswalk

* Read in crosswalk
qui import excel "`datapath'/cip1985to2000.xls", clear sheet("`crosswalk'") firstrow

* some edits and checks
rename `var_cipstart' cipcode`startyr'
rename `var_cipend' cipcode`endyr'
rename `var_titlestart' ciptitle`startyr'
rename `var_titleend' ciptitle`endyr'

qui replace cipcode`startyr' = strtrim(cipcode`startyr')
qui replace cipcode`endyr' = strtrim(cipcode`endyr')

if `yr' >= 1990 & `yr' < 2000 {
	gen cipdelete2000 = (regexm(ciptitle2000,"[D|d]elete") | regexm(cipcode2000,"[D|d]elete"))
	qui replace cipcode2000 = "01." if cipcode1990 == "02." 
	qui replace cipcode2000 = "01.11" if cipcode1990 == "02.04" 
	qui replace cipcode2000 = "" if cipcode1990 == "04.07" & cipdelete2000 == 1
	qui replace cipcode2000 = "52." if cipcode1990 == "08." 
	qui replace cipcode2000 = "54.01" if cipcode1990 == "45.08"
	qui replace cipcode2000 = "" if cipcode1990 == "12.02"
	qui replace cipcode2000 = "19." if cipcode1990 == "20."
	* Check the above and keep going!
	qui drop if regexm(cipcode2000,"and")
	qui drop if regexm(cipcode2000,"CHAPTER")
}

gen ciplen = strlen(regexr(cipcode`startyr',"\.",""))
qui summ ciplen
local cip6only = (`r(min)' == 6 & `r(max)' == 6)
assert ciplen == 6 | ciplen == 4 | ciplen == 2 | ciplen == 0

qui drop if cipcode`startyr' == ""

* Create 6 digit cross walk
preserve
drop ciplen

qui tempfile crosswalk`startyr'to`endyr'
qui save `crosswalk`startyr'to`endyr'', replace
restore

* If possible, generate 2- and 4-digit cip concordance
if `cip6only' == 0 {
	preserve
	qui keep if ciplen == 4
	rename cipcode`startyr' cipcode`startyr'_4
	rename cipcode`endyr' cipcode`endyr'_4
	drop ciplen

	qui tempfile crosswalk`startyr'to`endyr'_4
	qui save `crosswalk`startyr'to`endyr'_4', replace
	restore

	preserve
	qui keep if ciplen == 2
	rename cipcode`startyr' cipcode`startyr'_2
	rename cipcode`endyr' cipcode`endyr'_2
	drop ciplen

	qui tempfile crosswalk`startyr'to`endyr'_2
	qui save `crosswalk`startyr'to`endyr'_2', replace
	restore
}
else {
	clear
	gen cipcode`startyr' = .
	qui tempfile crosswalk`startyr'to`endyr'_4
	qui save `crosswalk`startyr'to`endyr'_4', replace
	qui tempfile crosswalk`startyr'to`endyr'_2
	qui save `crosswalk`startyr'to`endyr'_2', replace
}

**********************************
* B. Read in dictionary of values

qui insheet using "`datapath'/`yr'/dict/cip`yr'.txt", clear nonames

* Some necessary edits
foreach var of varlist * {
	qui replace `var' = strtrim(`var')
}

rename v1 ciptitle`startyr'
rename v2 cipcode`startyr'
qui drop in 1
qui drop if cipcode`startyr'==""

gen temp = regexr(v3,",","")
qui destring(temp), gen(freq)
drop temp v3

gen temp = regexr(v4,"%","")
qui destring(temp), gen(perc)
drop temp v4

qui drop if cipcode`startyr' == "99.0000" | cipcode`startyr' == "95.0000"


*************************
* C. Merge on 6 digit CIP

qui merge 1:1 cipcode`startyr' using `crosswalk`startyr'to`endyr''

* note: we only care about master (_merge 1 or 3))
qui drop if _merge == 2

qui egen tot_miss = total(perc) if _merge  == 1 
qui summ tot_miss
if `r(mean)' != . {
	local percno = `r(mean)'
}
else {
	local percno = 0
}
qui count if cipcode`endyr' == ""
local count_miss = `r(N)'
di "Missing " %5.0fc `count_miss' " 6-digit CIP codes in `yr'; " %4.2fc `percno' "% of data."
drop tot_miss
* Missing 34.78 percent of 6-digit CIP codes in 1990


drop _merge

*************************
* D. Merge on 4 digit CIP

if `cip6only' == 0 {

gen cipcode`startyr'_4 = substr(cipcode`startyr',1,5) 
order ciptitle`startyr' cipcode`startyr' cipcode`startyr'_4 perc cipcode`endyr'  

qui merge m:1 cipcode`startyr'_4 using `crosswalk`startyr'to`endyr'_4'

qui drop if _merge == 2

* Total missing four digit 
qui egen tot_miss = total(perc) if _merge  == 1 
qui summ tot_miss
if `r(mean)' != . {
	local percno = `r(mean)'
}
else {
	local percno = 0
}
qui count if cipcode`endyr'_4 == ""
local count_miss = `r(N)'
di "Missing " %5.0fc `count_miss' " 4-digit CIP codes in `yr'; " %4.2fc `percno' "% of data."
drop tot_miss

* Total missing four digit 
qui egen tot_found = total(perc) if _merge == 3 & cipcode`endyr' == ""
qui summ tot_found
if `r(mean)' != . {
	local percno = `r(mean)'
}
else {
	local percno = 0
}
qui count if cipcode`endyr' == ""
local count_miss = `r(N)'
qui count if cipcode`endyr' == "" & cipcode`endyr'_4 != ""
local found_count = `r(N)'
di %5.0fc `found_count' " of " %5.0fc `count_miss' " missing 6-digit CIP codes have 4-digit CIP codes (" %4.2fc `percno' "% of data)"
drop tot_found

}

}
