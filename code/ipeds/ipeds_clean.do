capture restore
set more off
set type double
clear all

cd "Z:\hcs"
*do Z:\hcs\code\ipeds\ipeds_clean.do

local datapath "data/ipeds"

local tempcode 0

*insheet using C:\Users\tasulliv.AD\Downloads\C2018_A\c2018_a.csv, clear
*insheet using Z:\hcs\data\ipeds\2016\c2016_a_data_stata.csv, clear

insheet using "`datapath'/1984/c1984_cip_data_stata.csv", clear
rename crace15 ctotalm
rename crace16 ctotalw
gen year = 1984

save "`datapath'/ipeds_c_all.dta", replace

forvalues yr = 1985/2018 {
	* Adjust for file names
	if (`yr' <= 1994 & `yr' != 1990) {
		local fyr = "c`yr'_cip_data_stata"
	}
	else if `yr' == 1990 {
		local fyr = "c8990cip_data_stata"
	}
	else if (`yr' >= 1995 & `yr' <=1999) {
		local fn = (`yr'-1900-1)*100 + (`yr'-1900)
		local fyr = "c`fn'_a_data_stata"
	}
	else if (`yr' >= 2000 & `yr' <= 2011) {
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

	if `yr' <= 2001 {
		local keepvars ctotalm ctotalw
	}
	else {
		local keepvars majornum ctotalm ctotalw
	}

	preserve

	di "reading `fyr'" 
	insheet using "`datapath'/`yr'/`fyr'.csv", clear

	if `yr' <= 2007 {
		rename crace15 ctotalm
	 	rename crace16 ctotalw
	}

	keep unitid cipcode awlevel `keepvars'

	gen year = `yr'

	tempfile yrfile
	save `yrfile', replace

	restore
	append using `yrfile'

}

save "`datapath'/ipeds_c_all.dta", replace

* Stuff for later
*local econ 450601 450602 450603 450604 450605 450699
*local econ_flag : subinstr local econ " " " | cipcode == ", all
*gen econ_flag = (cipcode == `econ_flag')

* 4-digit cip code
*tostring cipcode, gen(cip_str)
*gen cipmaj = substr(cip_str,1,4)
*drop cip_str
*order unitid cipcode cipmaj
