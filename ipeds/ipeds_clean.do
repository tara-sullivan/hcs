capture restore
set more off
set type double
clear all

local readdata 1
* note: might want to remove cipnames local;

if "`c(os)'" == "MacOSX" {
	cd "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/"
}
else {
	cd "Z:\hcs"
}

*global runit do Z:\hcs\code\ipeds\ipeds_clean.do
*do Z:\hcs\code\ipeds\ipeds_clean.do
*do "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/code/ipeds/ipeds_clean.do"

local datapath "data/ipeds"
local rawpath "`datapath'/raw"
local cippath "`datapath'/cip_edit"
local savepath "`datapath'"

*insheet using Z:\hcs\data\ipeds\2005\c2005_a_data_stata.csv, clear nonames

* initialize dataset
clear all
tempfile master_data
save `master_data', emptyok

if `readdata' {

forvalues yr = 1990/2018 {

	di "********"
	di "* `yr' *"
	di "********"

	* for cip codes
	if `yr' < 1990 {
	local startyr = 1985
	local endyr = 1990		
	}
	else if `yr' >= 1990 & `yr' < 2000 {
	local startyr = 1990
	local endyr = 2000		
	}
	else if `yr' >= 2000 & `yr' < 2010 {
	local startyr = 2000
	local endyr = 2010	
	}

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
	if `yr' < 2001 {
		local keepvars ctotalm ctotalw
	}
	else {
		local keepvars majornum ctotalm ctotalw
	}

	di "reading `fyr'..." 
	qui import delimited using "`rawpath'/`yr'/`fyr'.csv", clear varnames(nonames)

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

	* if there's no dot in the cip code, create a dot. also trim values
	qui replace cipcode = strtrim(cipcode)
	gen ciplen = strlen(cipcode)
	qui summ ciplen
	if `r(max)' == 6 {
		qui replace cipcode = substr(cipcode,1,2) + "." + substr(cipcode,3,.)
	}
	drop ciplen
	

	keep unitid cipcode awlevel `keepvars'
	gen year = `yr'
	qui destring awlevel, replace
	capture destring majornum, replace

	

	* locals to flag all aggregate cips 
	local agg_cips (cipcode == "99.0000" | cipcode == "95.0000" | cipcode == "95.9500" | cipcode == "99." | cipcode == "99")
	local not_agg_cips (cipcode != "99.0000" & cipcode != "95.0000" & cipcode != "95.9500" & cipcode != "99." & cipcode != "99")

	* useful variables for checking how much data are lost
	qui destring ctotal*, replace
	egen ctot = rowtotal(ctotalm ctotalw)
	qui egen tot = total(ctot) if `not_agg_cips'


	* merge in the updated cipcode for years before 2010 (will need to repeat this)
	* start here!
	if `yr' < 2010 {
		* merge in appropriate `yr' cipcodes
		gen cipcode`startyr'_d`yr' = cipcode
		qui merge m:1 cipcode`startyr'_d`yr' using "`cippath'/cip`yr'"
		qui drop if _merge == 2
		qui count if _merge == 1 & `not_agg_cips' 
		if `r(N)' != 0 {
			di "Missing " `r(N)' " observations from dictionary."
			qui levelsof cipcode if _merge == 1 & `not_agg_cips', clean local(miss_cip)
			di "Missing CIP codes: " "`miss_cip'"
		}
		else {
			assert `agg_cips' if _merge == 1 
		}
		drop _merge cipcode`startyr'_d`yr' ciptitle`startyr' ciptitle`startyr'_d update_flag
	}
	* merge in the 2000 cipcodes for 1990 data
	if `yr' < 2000 {
		* merge in 2000 cipcodes
		qui merge m:1 cipcode1990 using "`cippath'/crosswalk1990to2000"
		qui drop if _merge == 2
		* note that you might have cipcodes that are missing here; these are the ones 
		* I check for at the end of the merge file
		* Find number and percent of missing observations
		qui count if cipcode2000=="" & cipdelete != 1 & `not_agg_cips'
		local miss_cip = `r(N)'
		* percent of data
		qui count if cipdelete != 1 & `not_agg_cips'
		local perc = (`miss_cip'/`r(N)')*100
		* percent of students
		qui egen tot_miss = total(ctot) if cipcode2000 == "" & cipdelete != 1 & `not_agg_cips'
		qui summ tot_miss
		local miss_student = `r(mean)'
		qui summ tot
		local student = `r(mean)'
		local perc_student = (`miss_student'/`student')*100
		di %7.0fc `miss_cip' " observations missing 2000 CIP codes (" %4.2fc `perc' "% of data; " %4.2fc `perc_student' "% of students)"  
		* drop variables
		drop _merge ciptitle1990_cw ciptitle2000_cw cipdelete tot_miss
	}

	if `yr' < 2010 {
		qui merge m:1 cipcode2000 using "`cippath'/crosswalk2000to2010"
		qui drop if _merge == 2
		* Find number and percent of missing observations
		qui count if cipcode2010=="" & `not_agg_cips'
		local miss_cip = `r(N)'
		qui count if `not_agg_cips'
		local perc = (`miss_cip'/`r(N)')*100
		* percent of students missing
		qui egen tot_miss = total(ctot) if cipcode2010 == "" & cipdelete != 1 & `not_agg_cips'
		qui summ tot_miss
		if `r(N)' != 0 {
			local miss_student = `r(mean)'
			qui summ tot
			local student = `r(mean)'
			local perc_student = (`miss_student'/`student')*100
		}
		else {
			local perc_student = 0
		}

		di %7.0fc `miss_cip' " observations missing 2010 CIP codes (" %4.2fc `perc' "% of data; " %4.3fc `perc_student' "% of students)"  
		* drop unnecessary variables
		drop _merge ciptitle2000_cw ciptitle2010_cw cipdelete Action Textchang tot_miss
	}
	if `yr' >= 2010 {
		gen cipcode2010 = cipcode
	}

	keep year unitid cipcode awlevel `keepvars' cipcode2010

	qui append using `master_data'
	qui save `"`master_data'"', replace
}

order year unitid cipcode cipcode2010 awlevel majornum
sort unitid cipcode awlevel year majornum

qui save "`savepath'/ipeds_c_all.dta", replace

} // end readdata local

else{
	use "`savepath'/ipeds_c_all.dta", clear
}

