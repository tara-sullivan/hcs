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

*do Z:\hcs\code\ipeds\ipeds_clean.do
*do "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/code/ipeds/ipeds_clean.do"

local datapath "data/ipeds"

*insheet using C:\Users\tasulliv.AD\Downloads\C2018_A\c2018_a.csv, clear
*insheet using Z:\hcs\data\ipeds\2005\c2005_a_data_stata.csv, clear nonames

if `readdata' {

*insheet using "`datapath'/1984/c1984_cip_data_stata.csv", clear nonames
** this is a work around to keep leading zeros
*ds *
*foreach var of varlist `r(varlist)' {
	*local varname : di `var'
	*rename `var' `varname'
*}
*drop in 1
*rename *, lower
*
*rename crace15 ctotalm
*rename crace16 ctotalw
*gen year = 1984
*
*save "`datapath'/ipeds_c_all.dta", replace

local i = 1
forvalues yr = 1984/2018 {
	* Adjust for file names
	if (`yr' <= 1994 & `yr' != 1990) {
		*local fyr = "c`yr'_cip_data_stata"
		local fyr = "c`yr'_cip"
	}
	else if `yr' == 1990 {
		local fyr = "c8990cip"
	}
	else if (`yr' >= 1995 & `yr' <=1999) {
		local fn = (`yr'-1900-1)*100 + (`yr'-1900)
		*local fyr = "c`fn'_a_data_stata"
		local fyr = "c`fn'_a"
	}
	else if (`yr' >= 2000 & `yr' <= 2005) {
		local fyr = "c`yr'_a"
	}
	else if (`yr' >= 2006 & `yr' <= 2011) {
		local fyr = "c`yr'_a_data_stata"
	}
	else if (`yr' != 2016 & (`yr' >= 2012 & `yr' <= 2017)) {
		local fyr = "c`yr'_a_rv_data_stata"
	}
	else if `yr' == 2016 {
		local fyr = "c`yr'_a_rv"
	}
	else if `yr' == 2018 {
		local fyr = "c`yr'_a_data_stata"
	}

	* keep extra variables in years after 2007
	if `yr' <= 2001 {
		local keepvars ctotalm ctotalw
	}
	else {
		local keepvars majornum ctotalm ctotalw
	}

	if `i' > 1 {
		preserve
	}

	di "reading `fyr'..." 
	insheet using "`datapath'/`yr'/`fyr'.csv", clear nonames

	* this is a work around to keep leading zeros
	qui ds *
	foreach var of varlist `r(varlist)' {
		local varname : di `var'
		rename `var' `varname'
	}
	qui drop in 1
	qui rename *, lower

	* rename variables so they are consistent
	if `yr' <= 2007 {
		rename crace15 ctotalm
	 	rename crace16 ctotalw
	}

	keep unitid cipcode awlevel `keepvars'
	gen year = `yr'

	if `i' > 1 {
		tempfile yrfile
		qui save `yrfile', replace

		restore
		append using `yrfile'
	}
	
	qui save "`datapath'/ipeds_c_all.dta", replace

	local i = `i' + 1
}

} // end readdata local

else{
	use "`datapath'/ipeds_c_all.dta", clear

}

if `cipnames' {

* for blank names:
* import excel "`datapath'/cip2000to2010.xls", clear sheet("CIP2000")

********************************************************************************
* 1985 to 1990 concordance
import excel "`datapath'/cip1985to2000.xls", clear sheet("Crosswalk_CIP85toCIP90") firstrow

* some edits and checks
rename CIP85 cipcode1985
rename CIP90 cipcode1990

replace cipcode1985 = strtrim(cipcode1985)
replace cipcode1990 = strtrim(cipcode1990)

gen ciplen = strlen(regexr(cipcode1985,"\.",""))
assert ciplen == 0 | ciplen == 2 | ciplen == 4 | ciplen == 6

* keep concordance

keep cipcode1985 cipcode1990

tempfile cip1985to1990
save `cip1985to1990'


********************************************************************************
* 1990 to 2000 concordance
import excel "`datapath'/cip1985to2000.xls", clear sheet("Crosswalk_CIP90toCIP2K") firstrow

* some edits and checks
rename CIPCODE90 cipcode1990
rename CIPCODE2k cipcode2000

replace cipcode1990 = strtrim(cipcode1990)
replace cipcode2000 = strtrim(cipcode2000)

replace cipcode2000 = "54.01" if cipcode1990 == "45.08"
gen action1990 = "Deleted" if regexm(cipcode2000,"Deleted")
replace cipcode2000 = "" if regexm(cipcode2000,"Deleted")
drop if regexm(cipcode2000,"and")
drop if regexm(cipcode2000,"CHAPTER")

gen ciplen = strlen(regexr(cipcode2000,"\.",""))
assert ciplen == 0 | ciplen == 2 | ciplen == 4 | ciplen == 6
drop ciplen

gen ciplen = strlen(regexr(cipcode1990,"\.",""))
assert ciplen == 0 | ciplen == 2 | ciplen == 4 | ciplen == 6
drop ciplen

* generate concordance

drop if cipcode1990 == ""

keep cipcode1990 cipcode2000

tempfile cip1990to2000
save `cip1990to2000'

********************************************************************************
* 2000 to 2010 concordance 
import excel "`datapath'/cip2000to2010.xlsx", clear firstrow

* some edits and checks
qui rename *, lower

replace cipcode2010 = strtrim(cipcode2010)
replace cipcode2000 = strtrim(cipcode2000)

gen ciplen = strlen(regexr(cipcode2000,"\.",""))
assert ciplen == 0 | ciplen == 2 | ciplen == 4 | ciplen == 6

drop if cipcode2000 == ""

* rename and save concordance
rename action action2000 
rename textchange text2000
keep cipcode2000 cipcode2010 action text

tempfile cip2000to2010
save `cip2000to2010'

********************************************************************************
* 2010 concordance cip names
import excel "`datapath'/cip2000to2010.xlsx", clear firstrow

qui rename *, lower
keep cipcode2010 ciptitle2010
duplicates drop

gen ciplen = strlen(regexr(cipcode2010,"\.",""))

forvalues i = 2(2)4 {
	preserve
	keep if ciplen == `i'
	
	keep cipcode2010 ciptitle2010

	rename cipcode2010 cip`i'
	rename ciptitle2010 cip`i'name

	label var cip`i' "`i'-digit CIP code"
	label var cip`i'name "CIP `i'-digit title (2010)"

	tempfile cip`i'
	save `cip`i'', replace
	restore
}

* for consistency, 2-digits should end be formatted 01., not 01
replace cipcode2010 = cipcode2010 + "." if regexm(cipcode2010,"^[0-9][0-9]$")


tempfile cip2010names
save `cip2010names', replace

********************************************************************************
* Merge in appropriate CIP names concordances
* 1. Do some checks 
* 2. Merge in 2010 CIP code
* 3. Merge in 2010 CIP name

use "`datapath'/ipeds_c_all.dta", clear

replace cipcode = strtrim(cipcode)
* for now i'm not worrying about the ones with 5 digit cip codes
drop if year < 1987

*******************
* 1. Do some checks 

* check length of cip code; investigate each of these 
gen ciplength = strlen(cipcode)
 
* the two digit should only be equal to 99
assert cipcode == "99" if ciplength == 2

* the seven digit cip codes should contain a dot
gen hasdot = regexm(cipcode,"\.")
assert hasdot if ciplength == 7
assert !hasdot if ciplength == 6

* insert dot in cip code
replace cipcode = substr(cipcode,1,2) + "." + substr(cipcode,3,6) if ciplength == 6
replace ciplength = strlen(cipcode)
* I run into the five digit cip code problem in 1984-86
tab ciplength if cipcode != "99" & year >= 1987
assert `r(r)' == 1 

replace cipcode = "99" if cipcode == "99.0000"
drop ciplength hasdot

***************************
* 2. Merge in 2010 CIP code
* 2.A. Merge in 1990 CIP code
* 2.B. Merge in 2000 CIP code
* 2.C. Merge in 2010 CIP code

* Start here!
*****************************
* 2.A. Merge in 1990 CIP code

gen cipcode1985 = cipcode if  year < 1990
merge m:1 cipcode1985 using `cip1985to1990'
tab _merge if (year < 1990) & cipcode != "99"
*br if (year < 1990) & cipcode != "99" & _merge != 3
tab year if (year < 1990) & cipcode != "99" & _merge != 3

 gen cipcode2000 = cipcode if (year >= 2000 & year < 2010)
 merge m:1 cipcode2000 using `cip2000to2010'

 tab _merge if (year >= 2000 & year < 2010) & cipcode != "99"
 * notice that 3.88% dont have a match


* generate two digit and four digit cip codes
gen cip2 = substr(cipcode,1,2)
gen cip4 = substr(cipcode,1,5)

* merge in two digit cip code
merge m:1 cip2 using `cip2'

* check two digit merge
assert cip2 == "99" if _merge == 1
drop if _merge != 3
drop _merge

* merge in four digit cip code
merge m:1 cip4 using `cip4'
drop if _merge != 3
drop _merge

} // end cipnames local
