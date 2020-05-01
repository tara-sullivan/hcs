capture restore
set more off
set type double
clear all

local readdata 1
local cipnames 0

if "`c(os)'" == "MacOSX" {
	cd "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/"
}
else {
	cd "Z:\hcs"

}

*global runit do Z:\hcs\code\ipeds\ipeds_cip_merge.do
*do Z:\hcs\code\ipeds\ipeds_cip_merge.do
*do "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/code/ipeds/ipeds_clean.do"

local datapath "data/ipeds/raw"
local savepath "data/ipeds/cip_edit"


/*******************************************************************************
** Missing from concordance

I have data on completion rates of degree programs by institution and year. 
My data comes from here:
*https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx
Programs are identified by their CIP codes. 
These CIP codes change over time. 
Thus, to study how major composition changes over time,
I need to appropriately update CIP codes. 

There are four eras of CIP codes: 
A. 1985 to 1990
B. 1990 to 2000
C. 2000 to 2010
D. 2010 to 2020

To create a concordance between the three files, I use three files for each year.

1. The dictionary

Each year has a data dictionary available at the same location as the data. 
Sometimes this data is an excel file, sometimes it's an html page.
If that is the case, I've copied and pasted it into a .txt file. 

2. The crosswalk

The concordance provided by IPEDS are called "crosswalks."
Crosswalks are available here: 
https://nces.ed.gov/ipeds/cipcode/resources.aspx?y=56

3. The crosswalk dictionary

The crosswalk files often have separate dictionary files. 
The information here is largely the same as in the crosswalk file, but for one year.
The advantage of using this resources is that it avoids confusion when translating
between the dictionary file and the crosswalk file.
It also provides another resource for chekcing for errors. 

To find best cipcode for a particular year:
*A. Save crosswalk files 
*B. Read in dictionary of values
*C. Determine which CIP codes are missing from the crosswalk
*D. Manually update CIP codes (this step has some assumptions in it)
*E. Save concordance
*F. Check merge on 6 digit CIP
*G. Check merge on 4 digit CIP


*******************************************************************************/

*************************
* A. Save crosswalk files

foreach yr of numlist 1985 1990 2000 {
if `yr' == 1985 {
	local startyr = 1985
	local endyr = 1990
	local crosswalk_file "cip1985to2000.xls"
	local crosswalk_sheet "Crosswalk_CIP85toCIP90"
	local var_cipstart "CIP85"
	local var_cipend "CIP90"
	local var_titlestart "CIPTITLE85"
	local var_titleend "CIPTITLE90"
	local cw_dict_file "cip1985to2000.xls"
	local cw_dict_sheet "CIP1985"
}
if `yr' == 1990 {
	local startyr = 1990
	local endyr = 2000
	local crosswalk_file "cip1985to2000.xls"
	local crosswalk_sheet "Crosswalk_CIP90toCIP2K"
	local var_cipstart "CIPCODE90"
	local var_cipend "CIPCODE2k"
	local var_titlestart "CIPTEXT90"
	local var_titleend "CIPTEXT2K"
	local cw_dict_file "cip1985to2000.xls"
	local cw_dict_sheet "CIP1990"
}
if `yr' == 2000 {
	local startyr = 2000
	local endyr = 2010
	local crosswalk_file "cip2000to2010.xlsx"
	local crosswalk_sheet "Crosswalk2000to2010"
	local var_cipstart "CIPCode2000"
	local var_cipend "CIPCode2010"
	local var_titlestart "CIPTitle2000"
	local var_titleend "CIPTitle2010"
	local cw_dict_file "cip1985to2000.xls"
	local cw_dict_sheet "CIP2000"
}


di "************************"
di "* `yr' crosswalk files *"
di "************************"

* Read in crosswalk
qui import excel "`datapath'/`crosswalk_file'", clear sheet("`crosswalk_sheet'") firstrow

* some edits and checks
rename `var_cipstart' cipcode`startyr'
rename `var_cipend' cipcode`endyr'
rename `var_titlestart' ciptitle`startyr'_cw
rename `var_titleend' ciptitle`endyr'_cw

qui replace cipcode`startyr' = strtrim(cipcode`startyr')
qui replace cipcode`endyr' = strtrim(cipcode`endyr')

if `yr' == 1990 {
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
else if `yr' == 2000 {
	qui replace cipcode2010 = "" if Action == "Deleted"
	gen cipdelete = (Action == "Deleted")
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

save "`savepath'/crosswalk`startyr'to`endyr'", replace
restore

* 4-digit cip concordance
preserve
qui keep if ciplen == 4
rename cipcode`startyr' cipcode`startyr'_4
rename cipcode`endyr' cipcode`endyr'_4
drop ciplen

save "`savepath'/crosswalk`startyr'to`endyr'_4", replace
restore

* 2-digit concordance
preserve
qui keep if ciplen == 2
rename cipcode`startyr' cipcode`startyr'_2
rename cipcode`endyr' cipcode`endyr'_2
drop ciplen
save "`savepath'/crosswalk`startyr'to`endyr'_2", replace
restore


* Save crosswalk dictionaries


qui import excel "`datapath'/`cw_dict_file'", clear sheet("`cw_dict_sheet'") firstrow



drop CIPFAMILY
*capture drop CIPDESCR 
capture drop CIPNODOT
capture drop ID

qui ds *, has(type string)
foreach var of varlist `r(varlist)' {
	qui replace `var' = strtrim(`var')
	qui replace `var' = stritrim(`var')
}

rename CIPTITLE ciptitle`yr'_cwd

if `yr' != 2000 {
	local y : subinstr local yr "19" ""
	rename CIP`y' cipcode`yr'
}
else if `yr' == 2000 {
	* Note: spreadsheet contains 1990 cip codes that move in 2000, and doesn't differentiate those from 2000 cipcodes
	rename CIPCode cipcode`yr'

	qui drop if cipcode2000 == "01.11" & ACTIONCODE == "M"
	qui drop if cipcode2000 == "01.1201" & ciptitle`yr'_cwd == "(Moved from 02."
	qui drop if cipcode2000 == "21." & ciptitle`yr'_cwd == "Programs for Series 21."
	qui drop if cipcode2000 == "28." & ciptitle`yr'_cwd == "Programs for Series 28."
	qui drop if cipcode2000 == "53." & ciptitle`yr'_cwd == "Programs for Series 53."
	qui drop if cipcode2000 == ""
	qui replace ReportUnder = "" if cipcode`yr' == "11.02"
	qui replace ReportUnder = "31.0301" if ReportUnder == "1. 0301"
	qui replace ReportUnder = "26.04" if ReportUnder == "26.02" & CIPDESCR == "(Report under 26.04 Series)"
	qui replace ReportUnder = "38.0206" if ReportUnder == "38.020" & CIPDESCR == "(Report under 38.0206"
	qui replace ReportUnder = "52.09" if ReportUnder == "53.09" & CIPDESCR == "(Report under 52.09 Series)"
	qui replace ReportUnder = "15.0611" if ReportUnder == "15.061" & CIPDESCR == "(Report under 15.0611"
	qui replace ReportUnder = "" if ReportUnder == "52.1" & CIPDESCR == "(Report under appropriate code in 52.18 or 52.19 Series)"
	qui replace ReportUnder = "51.15" if ReportUnder == "52.15" & CIPDESCR == "(Report under 51.15 Series)"
	qui replace ReportUnder = "30.1601" if ReportUnder == "0.1601)"
	qui replace ReportUnder = "16.03" if ReportUnder == "16.21"
	qui replace ReportUnder = "16.11" if ReportUnder == "16.24"

	qui drop if regexm(cipcode`yr',"^----") & ReportUnder == ""
	qui drop if regexm(cipcode`yr',"[a-zA-Z]") 
	qui drop if regexm(ReportUnder,"[a-zA-Z]")

	qui drop if ACTIONCODE == "D"

	* find all old 1990 cip codes that are reported under new 2000 values 
	qui replace CIPDESCR = "(Report under 31.0301)" if CIPDESCR == "(Report under 31. 0301)"
	qui replace CIPDESCR = "(Report under 16.1603)" if CIPDESCR == "1603)"
	qui replace CIPDESCR = "(Report under 52.)" if CIPDESCR == "(Report under appropriate code in 52. Series)"
	qui replace CIPDESCR = "(Report under 13.0202)" if CIPDESCR == "(Report under 13.0201 or 13.0202)"
	qui replace CIPDESCR = "(Report under 19.0702)" if CIPDESCR == "0702)"
	qui replace CIPDESCR = "(Report under 22.)" if CIPDESCR == "(Report under to 22. Series)"
	qui replace CIPDESCR = "(Report under 51.0803)" if CIPDESCR == "(Report under to 51.0803)"
	qui gen moveno = regexs(2) if regexm(CIPDESCR,"([R|r]eport under )([0-9][0-9]\.?[0-9]*)") 

	* find 2000 cipcodes that certain line item move to
	qui levelsof moveno if ACTIONCODE == "M", local(cip_move)
	qui gen movematch = moveno if ACTIONCODE == "M" & moveno != ""
	foreach cip in `cip_move' {
		qui replace movematch = "`cip'" if cipcode2000 == "`cip'" & movematch == ""
	}
	* check that all of the moved cip codes are in the data twice
	qui duplicates tag movematch, gen(dup)
	assert dup == 1 if movematch != ""
	* keep only the current cip code
	qui drop if movematch != "" & (movematch != cipcode2000)
	drop dup movematch

	* find remaining cases where the moveno doesn't match reportunder
	assert moveno == ReportUnder if (moveno != "16.21" & moveno != "16.24")
	drop moveno

	* assert everything in ReportUnder matches a cipcode, so we can drop all of those
	qui levelsof ReportUnder, local(cip_move)
	qui gen tempcode = ReportUnder if ReportUnder != ""
	foreach cip in `cip_move' {
		qui replace tempcode = "`cip'" if cipcode2000 == "`cip'"
	}
	qui levelsof tempcode, local(groups)
	gen keepme = (tempcode == "")
	foreach group in `groups' {
		qui replace keepme = 1 if cipcode2000 == tempcode
	}
	* check that every group has at least only one item being kept
	bys tempcode: egen max_keepme = max(keepme)
	qui summ max_keepme
	assert `r(min)' == `r(max)'
	qui keep if keepme == 1
	drop ACTIONCODE ReportUnder tempcode keepme max_keepme
}

capture drop CIPDESCR

gen year = `yr'

save "`savepath'/ciplist`yr'", replace

}

************************
* 2010 dictionary titles

di "********"
di "* 2010 *"
di "********"

qui import delimited "`datapath'/CIP2010", clear varnames(nonames)

* Some necessary edits
foreach var of varlist * {
	qui replace `var' = strtrim(`var')
}

rename v2 cipcode2010
rename v3 action
rename v5 ciptitle2010

qui drop in 1

drop if action == "Deleted" | action == "Moved to"
drop v1 action v4 v6 v7 v8

gen ciplen = strlen(regexr(cipcode2010,"\.",""))
foreach d of numlist 2 4 {
	preserve
	qui keep if ciplen == `d'

	drop ciplen

	qui replace ciptitle2010 = strtrim(ciptitle2010)
	qui replace ciptitle2010 = stritrim(ciptitle2010)

	qui compress

	rename cipcode2010 cip`d'
	save "`savepath'/cip`d'names", replace

	restore
}





**********************************
* B. Read in dictionary of values
foreach yr of numlist 1990/2009 {

if `yr' == 1987 {
	local startyr = 1985
	local endyr = 1990
}
if `yr' >= 1990 & `yr' < 2000 {
	local startyr_m1 = 1985
	local startyr = 1990
	local endyr = 2000
}
if `yr' >= 2000 {
	local startyr_m1 = 1990
	local startyr = 2000
	local endyr = 2010
}


di "********"
di "* `yr' *"
di "********"

* Read in official dictionary
if `yr' <= 2001 {
	qui insheet using "`datapath'/`yr'/dict/cip`yr'.txt", clear nonames
}
if `yr' == 2002 {
	import excel using "`datapath'/`yr'/dict/c`yr'_a.xls", clear allstring sheet("Frequencies")
	rename C v2
	rename D v1
	rename E v3
	rename F v4
	qui drop if B == "AWLEVEL" | B == "CIPCODE" | B == "MAJORNUM"
	drop A B 

}
if `yr' >= 2003 & `yr' <= 2005 {
	qui insheet using "`datapath'/`yr'/dict/c`yr'_a.txt", clear nonames
}
if `yr' >= 2006 & `yr' <= 2008 {
	import excel using "`datapath'/`yr'/dict/c`yr'_a.xlsx", clear allstring sheet("Frequencies")
	rename C v2
	rename D v1
	rename E v3
	rename F v4
	qui drop if B == "AWLEVEL" | B == "MAJORNUM"
	drop A B 
}
if `yr' >= 2009 {
	import excel using "`datapath'/`yr'/dict/c`yr'_a.xls", clear allstring sheet("FrequenciesRV")
	rename C v2
	rename D v1
	rename E v3
	rename F v4
	qui drop if B == "AWLEVEL" | B == "MAJORNUM"
	drop A B 
}


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

qui drop if cipcode`startyr' == "99.0000" | cipcode`startyr' == "95.0000" | cipcode`startyr' == "99"

*************************************************************
* C. Determine which CIP codes are missing from the crosswalk

* Create flag for original dictionary
gen dict = 1
gen cipcode`startyr'_d`yr' = cipcode`startyr'
order cipcode`startyr'_d`yr'

* Merge in startyr data
qui merge 1:1 cipcode`startyr' using "`savepath'/ciplist`startyr'"
rename _merge merge`startyr'

* Merge in startyr-1 data
drop year
qui gen year = `startyr_m1' if dict == 1
gen cipcode`startyr_m1' = cipcode`startyr' 
qui merge 1:1 year cipcode`startyr_m1' using "`savepath'/ciplist`startyr_m1'"
rename _merge merge`startyr_m1'

******************************
* D. Manually update CIP codes

* Compare merges in two years
di "`yr' CIP codes in `startyr' and `startyr_m1' crosswalk dictionaries"
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
* However, the Accounting line item in the data was 06.0201, the 1985 CIP
* For these cases, we assume that they are using the older, minus 1 number (m1),
* and that we need to update to the current, accurate CIP code. 
* Therefore we need to update those CIP codes using the crosswalk files. 
preserve
* keep the obs. that use old, m1 CIP codes. 
qui keep if merge`startyr' == 1 & merge`startyr_m1' == 3 & dict == 1
drop cipcode`startyr'
assert ciptitle`startyr'_cwd == ""
drop ciptitle`startyr'_cwd
order cipcode* ciptitle`startyr'_d ciptitle`startyr_m1'_cwd
* check here that cip codes from the dictionary match the old cip codes
* this means comparing the cip description from the dictionary in the current
* year (ciptitle`startyr'_d) to the description from the previous year's 
* crosswalk dictionary (ciptitle`startyr_m1'_cwd). 
* Once your've checked that this is a reasonable assumption, we need to update
* this old, m1 CIP code to the new current value. 
qui merge 1:1 cipcode`startyr_m1' using "`savepath'/crosswalk`startyr_m1'to`startyr'"
* We don't care about observations from the using data
qui drop if _merge == 2 
* Sometimes this process won't recover all codes. 
* Check here if you're running into weird problems. 
qui replace cipcode`startyr' = cipcode`startyr'_d`yr' if _merge == 1 & cipdelete != 1
qui replace cipcode`startyr' = cipcode`startyr'_d`yr' if _merge == 3 & cipdelete == 1
* We update the codes that match. Note that I updated cipcode`startyr' by 
* dropping it above and merging in new cipcode`startyr' via the crosswalk.
qui gen update_flag = (_merge == 3 & cipdelete != 1)
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
* E. Save updated cip codes

preserve
drop freq perc dict goodmerge
save "`savepath'/cip`yr'.dta", replace
restore


*******************************
* F. Check merge on 6 digit CIP

* note m:1 because, when you update cip codes you may have duplicates
qui merge m:1 cipcode`startyr' using "`savepath'/crosswalk`startyr'to`endyr'"

* note: we only care about master (_merge 1 or 3))
qui drop if _merge == 2

* check what's happening in the data
assert cipcode`endyr' == "" if _merge == 1
assert cipcode`endyr' == "" if (_merge == 3 & cipdelete == 1)
assert ((_merge == 1) | (_merge == 3 & cipdelete == 1)) if cipcode`endyr' == ""

* type out the missing results
qui egen tot_miss = total(perc) if ((_merge == 1) | (_merge == 3 & cipdelete == 1))
qui summ tot_miss
if `r(mean)' != . {
	local percno = `r(mean)'
}
else {
	local percno = 0
}
qui count if cipcode`endyr' == ""
local count_miss = `r(N)'
di "`yr' data missing " %5.0fc `count_miss' " 6-digit CIP codes in `endyr' crosswalk; " %4.2fc `percno' "% of data."
drop tot_miss
* Missing 34.78 percent of 6-digit CIP codes in 1990

rename cipdelete cipdelete6
drop _merge

*******************************
* G. Check merge on 4 digit CIP


* generate 4 digit from start year
gen cipcode`startyr'_4 = substr(cipcode`startyr',1,5) 

* merge on 4 digit from start year 
qui merge m:1 cipcode`startyr'_4 using "`savepath'/crosswalk`startyr'to`endyr'_4"

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
