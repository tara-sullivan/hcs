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


local datapath "data/ipeds"
local namepath "data/ipeds/cip_edit"

* Graph locals 
local graphregion "graphregion(color(white))"
local xlaboptions "labsize(small)"
local ylaboptions "angle(0) labsize(small)"
local axistitlesize "size(vsmall)"
local titleoptions "bexpand span justification(center) size(medlarge)"
local subtitleoptions "bexpand span justification(left) size(small)"
local captionoptions "bexpand span size(small)"
local xtitleoptions "size(small)"  
local legendoptions "bexpand span justification(left) size(small) region(lcolor(none)) symy(small) symx(small)"
local glocals `graphregion' title(, `titleoptions') ytitle(, size(small)) xtitle("") xlab(,`xlaboptions') ylab(`yaxisscale',`ylaboptions') legend(`legendlab' `legendoptions') caption(, size(small) justification(left) bexpand span)

* Read in data, do necessary cleaning
use "`datapath'/ipeds_c_all.dta", clear

* drop aggregate cip codes
local agg_cips (cipcode == "99.0000" | cipcode == "95.0000" | cipcode == "95.9500" | cipcode == "99." | cipcode == "99")
local not_agg_cips (cipcode != "99.0000" & cipcode != "95.0000" & cipcode != "95.9500" & cipcode != "99." & cipcode != "99")
drop if `agg_cips'

* keep only full time series
drop if cipcode2010 == ""

* keep only bachelor's degrees
keep if awlevel == 5
drop awlevel



* find out if there are any duplicates in bachelor degrees
duplicates tag year unitid cipcode majornum, gen(dup)
assert dup == 0
drop dup

* if there are two majors for a particular institution/cip, aggregate them
collapse (sum) ctotalm ctotalw, by(year unitid cipcode2010)

* generate two digit and four digit CIP codes
gen cip2 = substr(cipcode2010,1,2)
gen cip4 = substr(cipcode2010,1,5)

* create totals for 2-digit codes; make sure the trends look sensible
preserve

collapse (sum) ctotalm ctotalw, by(year)
egen ctotal = rowtotal(ctotalm ctotalw)

twoway line ctotal year, `glocals'





* total men and women over time by two digit cipcode
preserve

gen cip2 = substr(cipcode2010,1,2)
collapse (sum) ctotalm ctotalw, by(cip2 year)

* Add names
merge m:1 cip2 using "`namepath'/cip2names"
drop if _merge ==2 
assert _merge !=1
drop _merge
rename cip2 cip

bys cip: gen tot_yrs = _N
bys cip: egen min_yr = min(year)
gen temp = 2018 - tot_yrs + 1
drop if temp != min_yr
drop tot_yrs min_yr temp

* Make things shorter
replace ciptitle2010 = regexr(ciptitle2010,"\.","")
replace ciptitle2010 = strproper(ciptitle2010)
replace ciptitle2010 = "Agriculture and related sciences" if cip == "01"
replace ciptitle2010 = "Communications technologies and support services" if cip == "10"
replace ciptitle2010 = "Computer and information services" if cip == "11"
replace ciptitle2010 = "Engineering technologies" if cip == "15"
replace ciptitle2010 = "Liberal arts and sciences" if cip == "24"
replace ciptitle2010 = "Law enforcement and protective services" if cip == "43"
replace ciptitle2010 = "Business and related services" if cip == "52"
compress

* create variable label 
destring cip, replace
labmask cip, values(ciptitle2010)
drop ciptitle2010

* generate ratio
gen wmrat = ctotalw/ctotalm
drop ctotalm ctotalw


* Create a flag for low 
levelsof cip if wmrat < 1/2 & year == 1990, local(low_rat)
levelsof cip if wmrat > 3/2 & year == 1990, local(high_rat)

* Prepare for reshape: save the value labels for variables in local list
levelsof cip, local(cip_levels)
foreach val of local cip_levels {
	local cip`val'_lab : label cip `val'
}

reshape wide wmrat, i(year) j(cip)

* apply former value labels as variable labels
foreach var of local cip_levels {
	label var wmrat`var' "`cip`var'_lab'"
}

* graph shit
local legend legend(symy(small) symx(small)) 

local glocals graphregion(color(white)) `legend'

local graph_low : subinstr local low_rat " " " wmrat", all
twoway line wmrat`graph_low' year, `glocals'

local graph_high : subinstr local high_rat " " " wmrat", all
twoway line wmrat`graph_high' year, `glocals'

local trad_high 13 23 42

local trad_low 11 14 27 45 54 26
local graph_low : subinstr local trad_low " " " *", all
twoway line *`graph_low' year, `glocals'






/*

local datapath "data/ipeds"
local namepath "data/ipeds/cip_edit"
local rawpath "`datapath'/raw"

qui import delimited using "`rawpath'/2018/flags2018_data_stata.csv", clear varnames(nonames)

foreach var of varlist * {
	local `var'_name : di `var'
	rename `var' ``var'_name'
}
drop in 1

unique UNITID
* maybe stat_c = 1 | 4 and prch_c == 4?

qui import delimited using "`rawpath'/2018/c2018_a_data_stata.csv", clear varnames(nonames)

* this is a work around to keep leading zeros
qui ds *
foreach var of varlist `r(varlist)' {
	local varname : di `var'
	rename `var' `varname'
}
qui drop in 1
qui rename *, lower
qui replace cipcode = strtrim(cipcode)

unique unitid

*/
