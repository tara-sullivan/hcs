capture restore
set more off
set type double
clear all

*do Z:\hcs\code\ipeds\trends.do
*global runit do Z:\hcs\code\ipeds\trends.do

if "`c(os)'" == "MacOSX" {
	cd "/Users/tarasullivan/Google Drive File Stream/My Drive/research/hcs/"
}
else {
	cd "Z:\hcs"
}

* Stuff for later
*local econ 450601 450602 450603 450604 450605 450699
*local econ_flag : subinstr local econ " " " | cipcode == ", all
*gen econ_flag = (cipcode == `econ_flag')

* 4-digit cip code
*tostring cipcode, gen(cip_str)
*gen cipmaj = substr(cip_str,1,4)
*drop cip_str
*order unitid cipcode cipmaj

local datapath "data/ipeds"

use "`datapath'/ipeds_c_all.dta", clear

* keep only bachelor's degrees
keep if awlevel == 5
drop awlevel

* keep only full time series
drop if cipcode2010 == ""

* find out if there are any duplicates in bachelor degrees
duplicates tag unitid cipcode year, gen(dup)
duplicates tag unitid cipcode2010 year, gen(dup2)
assert dup2 == 1 if dup == 1
