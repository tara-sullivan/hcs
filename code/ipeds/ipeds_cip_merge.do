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

*/*******************************************************************************
** Missing from concordance
*
*Here I check which CIP codes are missing from the concordances. 
*There are three concordances:
*A. 1985 to 1990
*B. 1990 to 2000
*C. 2000 to 2010
*
*I also have lists of the CIP codes from the dictionaries here:
*https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx
*
*To find best cipcode for a particular year:
*A. Save crosswalk files 
*B. Read in dictionary of values
*C. Determine which CIP codes are missing from the crosswalk
*D. Manually update CIP codes
*E. Save concordance
*F. Check merge on 6 digit CIP
*G. Check merge on 4 digit CIP
*******************************************************************************/

*************************
* A. Save crosswalk files

foreach yr of numlist 1985 1990 {
if `yr' == 1985 {
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

di "************************"
di "* `yr' crosswalk files *"
di "************************"

* Read in crosswalk
qui import excel "`datapath'/cip1985to2000.xls", clear sheet("`crosswalk'") firstrow

* some edits and checks
rename `var_cipstart' cipcode`startyr'
rename `var_cipend' cipcode`endyr'
rename `var_titlestart' ciptitle`startyr'_cw
rename `var_titleend' ciptitle`endyr'_cw

qui replace cipcode`startyr' = strtrim(cipcode`startyr')
qui replace cipcode`endyr' = strtrim(cipcode`endyr')

if `yr' >= 1990 & `yr' < 2000 {
	gen cipdelete = (regexm(ciptitle2000_cw,"[D|d]elete") | regexm(cipcode2000,"[D|d]elete"))
	* 02.: reported under 01. and 26. series
	qui replace cipcode2000 = "" if cipcode1990 == "02." 
	qui replace cipcode2000 = "01.11" if cipcode1990 == "02.04" 
	qui replace cipcode2000 = "" if cipcode1990 == "04.07" & cipdelete == 1
	* 08.: reported under 52. series
	qui replace cipcode2000 = "" if cipcode1990 == "08." 
	qui replace cipcode2000 = "" if cipcode1990 == "12.02"
	* Report under 19. series
	qui replace cipcode2000 = "" if cipcode1990 == "20." 
	* Report under 26. series
	qui replace cipcode2000 = "" if cipcode1990 == "51.13" 
	* Report under 54.01 series
	qui replace cipcode2000 = "" if cipcode1990 == "45.08" 
	* Check the above and keep going!
	qui drop if regexm(cipcode2000,"and")
	qui drop if regexm(cipcode2000,"CHAPTER")
}
else {
	gen cipdelete = 0
}

gen ciplen = strlen(regexr(cipcode`startyr',"\.",""))
qui summ ciplen
assert ciplen == 6 | ciplen == 4 | ciplen == 2 | ciplen == 0

qui drop if cipcode`startyr' == ""

* Create 6 digit cross walk
preserve
qui keep if ciplen == 6
drop ciplen

qui tempfile crosswalk`startyr'to`endyr'
qui save `crosswalk`startyr'to`endyr'', replace
di "crosswalk" "`startyr'" "to" "`endyr'"
restore

* 4-digit cip concordance
preserve
qui keep if ciplen == 4
rename cipcode`startyr' cipcode`startyr'_4
rename cipcode`endyr' cipcode`endyr'_4
drop ciplen

qui tempfile crosswalk`startyr'to`endyr'_4
qui save `crosswalk`startyr'to`endyr'_4', replace
di "crosswalk" "`startyr'" "to" "`endyr'" "_4"
restore

* 2-digit concordance
preserve
qui keep if ciplen == 2
rename cipcode`startyr' cipcode`startyr'_2
rename cipcode`endyr' cipcode`endyr'_2
drop ciplen
qui tempfile crosswalk`startyr'to`endyr'_2
qui save `crosswalk`startyr'to`endyr'_2', replace
di "crosswalk" "`startyr'" "to" "`endyr'" "_2"
restore

* Save crosswalk dictionaries

qui import excel "`datapath'/cip1985to2000.xls", clear sheet("CIP`yr'") firstrow
drop CIPFAMILY CIPNODOT
capture drop CIPDESCR 

local y : subinstr local yr "19" ""
rename CIP`y' cipcode`yr'

rename CIPTITLE ciptitle`yr'_cwd

gen year = `yr'

qui tempfile ciplist`yr'
qui save "`ciplist`yr''", replace
di "ciplist" "`yr'"

}

**********************************
* B. Read in dictionary of values

foreach yr of numlist 1990/1999 {
if `yr' == 1987 {
	local startyr = 1985
	local endyr = 1990
	local crosswalk "Crosswalk_CIP85toCIP90"
	local var_cipstart "CIP85"
	local var_cipend "CIP90"
	local var_titlestart "CIPTITLE85"
	local var_titleend "CIPTITLE90"
}
if `yr' >= 1990 {
	local startyr_m1 = 1985
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

* Read in official dictionary
qui insheet using "`datapath'/`yr'/dict/cip`yr'.txt", clear nonames

* Some necessary edits
foreach var of varlist * {
	qui replace `var' = strtrim(`var')
}

rename v1 ciptitle`startyr'_d
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

*************************************************************
* C. Determine which CIP codes are missing from the crosswalk

* Create flag for original dictionary
gen dict = 1
gen cipcode`startyr'_d`yr' = cipcode`startyr'
order cipcode`startyr'_d`yr'

* Merge in startyr data
qui merge 1:1 cipcode`startyr' using `ciplist`startyr''
rename _merge merge`startyr'

* Merge in startyr-1 data
drop year
qui gen year = `startyr_m1' if dict == 1
gen cipcode`startyr_m1' = cipcode`startyr' 
qui merge 1:1 year cipcode`startyr_m1' using `ciplist`startyr_m1''
rename _merge merge`startyr_m1'

******************************
* D. Manually update CIP codes

* Compare merges in two years
di "`yr' CIP codes in `startyr' and `startyr_m1' crosswalk"
tab merge`startyr' merge`startyr_m1' if dict == 1
order cipcode* merge* ciptitle*

* Go through the categories of the merge, until everything is a good merge!
qui gen goodmerge = 0 if dict == 1

* OK if merged with both startyr and startyr-1
qui replace goodmerge = 1 if merge`startyr' == 3 & merge`startyr_m1' == 3

* in startyr, not in startyr-1: probably ok, do a quick check
qui replace goodmerge = 1 if merge`startyr' == 3 & merge`startyr_m1' == 1 & dict == 1
* br cipcode* ciptitle* if merge`startyr' == 3 & merge`startyr_m1' == 1 & dict == 1

* in startyr-1, not in startyr: definitely check
* Occasionally there was a lag in adpoting older numbers. 
* For instance, accounting had a CIP of 52.0301 in 1990. 
* However, the Accounting line item in the data was 06.0201.
preserve
qui keep if merge`startyr' == 1 & merge`startyr_m1' == 3 & dict == 1
drop cipcode`startyr' 
order cipcode* ciptitle`startyr'_d ciptitle`startyr_m1'_cwd
* check here that ciptitle match
qui merge 1:1 cipcode`startyr_m1' using `crosswalk`startyr_m1'to`startyr''
qui replace cipcode`startyr' = cipcode`startyr'_d`yr' if _merge == 1
qui drop if _merge == 2 
qui gen update_flag = (_merge == 3)
keep cipcode`startyr'_d`yr' cipcode`startyr' ciptitle`startyr'_d perc freq dict merge`startyr' merge`startyr_m1' goodmerge update_flag
qui replace goodmerge = 1 if update_flag == 1
qui tempfile update_cipcodes
qui save `update_cipcodes', replace
restore

qui drop if merge`startyr' == 1 & merge`startyr_m1' == 3 & dict == 1
qui append using `update_cipcodes'
order cipcode`startyr'_d cipcode`startyr'
sort cipcode`startyr'

*tab goodmerge if dict == 1

qui keep if dict == 1
keep cipcode`startyr'_d`yr' cipcode`startyr' ciptitle`startyr'_d freq perc dict goodmerge update_flag
*********************
* E. Save concordance

*******************************
* F. Check merge on 6 digit CIP

* note m:1 because, when you update cip codes you may have duplicates
qui merge m:1 cipcode`startyr' using `crosswalk`startyr'to`endyr''

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

assert cipcode`endyr' == "" if _merge == 1
assert ((_merge == 1 & cipdelete == .) | (_merge == 3 & cipdelete == 1)) if cipcode`endyr' == ""

rename cipdelete cipdelete6
drop _merge

*******************************
* G. Check merge on 4 digit CIP


* generate 4 digit from start year
gen cipcode`startyr'_4 = substr(cipcode`startyr',1,5) 

* merge on 4 digit from start year 
qui merge m:1 cipcode`startyr'_4 using `crosswalk`startyr'to`endyr'_4'

* delete this~
drop *title*

qui drop if _merge == 2

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
