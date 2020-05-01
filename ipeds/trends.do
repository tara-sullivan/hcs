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


local junk = 0 

********************************************************************************
* 1. Number of bachelor degrees 
* 2. Create 2-digit CIP dataset
* 3. Graph 2-digit CIP totals for men and women 

********************************************************************************
* File paths
local datapath "data/ipeds"
local namepath "data/ipeds/cip_edit"

* Graph locals 
local graphregion graphregion(color(white))
local gfont size(small)

local maintitle title(, bexpand span justification(center) size(medlarge))
local subtitleoptions subtitle(, bexpand span justification(left) `gfont')
local titleoptions `maintitle' `subtitleoptions' 

local axistitle ytitle(, `gfont')
local xlaboptions xlab(, lab`gfont')
local ylaboptions ylab(, angle(0) lab`gfont')
local axisoptions `axistitle' `xlaboptions' `ylaboptions'

local captionoptions caption(, `gfont' justification(left) bexpand span)

local wideleg bexpand span justification(left) 
local roptions region(lcolor(none)) symy(small) symx(small)
local legendoptions legend(`gfont' `roptions')

local glocals `graphregion' `titleoptions' `axisoptions' `legendoptions'

********************************************************************************
* Read in data, do necessary cleaning
use "`datapath'/ipeds_c_all.dta", clear

* label variables 
label var ctotalm "Men"
label var ctotalw "Women"

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

tempfile startfile
save `startfile', replace

********************************************************************************
* 1. Number of bachelor degrees by men and women

preserve

collapse (sum) ctotalm ctotalw, by(year)

foreach var of varlist ctotal* {
	replace `var' = `var'/1e6
}

* label variables 
label var ctotalm "Men"
label var ctotalw "Women"

local subt subtitle("Million degrees completed") xtitle("")
local legpos legend(ring(0) position(4) row(2))
twoway line ctotalm ctotalw year, `glocals'  `subt' `legpos'

restore

********************************************************************************
* 2. Create 2-digit CIP dataset

*preserve

collapse (sum) ctotalm ctotalw, by(cip2 year)

* list of 20 largest CIP codes
egen ctotal = rowtotal(ctotalm ctotalw)
gsort year -ctotal
bys year: gen rank = _n
levelsof cip2 if rank<=20 & year == 2018, local(top20) clean
levelsof cip2 if rank<=12 & year == 2018, local(top12) clean
drop rank ctotal

* Add names
merge m:1 cip2 using "`namepath'/cip2names"
drop if _merge ==2 
assert _merge !=1
drop _merge

* some weird observations end up there given my time series; drop those
bys cip2: gen tot_yrs = _N
bys cip2: egen min_yr = min(year)
gen temp = 2018 - tot_yrs + 1
drop if temp != min_yr
drop tot_yrs min_yr temp

* Make names shortker
replace ciptitle2010 = regexr(ciptitle2010,"\.","")
replace ciptitle2010 = strproper(ciptitle2010)
replace ciptitle2010 = "Agriculture and related sciences" if cip2 == "01"
replace ciptitle2010 = "Communications technologies and support services" if cip2 == "10"
replace ciptitle2010 = "Computer and information services" if cip2 == "11"
replace ciptitle2010 = "Engineering technologies" if cip2 == "15"
replace ciptitle2010 = "Liberal arts and sciences" if cip2 == "24"
replace ciptitle2010 = "Law enforcement and protective services" if cip2 == "43"
replace ciptitle2010 = "Business and related services" if cip2 == "52"
compress

* create variable label 
destring cip2, replace
labmask cip2, values(ciptitle2010)
drop ciptitle2010

* save time series for each of the top 20 cipcode

********************************************************************************
* 3. Graph 2-digit CIP totals for men and women 

gsort cip2 year

* In thousands
foreach var of varlist ctotal* {
	replace `var' = `var'/1e3
}

label var ctotalm "Men"
label var ctotalw "Women"

preserve
local keep12 : subinstr local top12 " " " | cip2 == ", all
keep if cip2 == `keep12'

gsort cip2 year
twoway line ctotalm ctotalw year, by(cip2, rows(4))

foreach cip of local top20 {
	* save the label of the graph
	local graph_name : label (cip2) `cip'

	* various options
	local topts title("`graph_name'") xtitle("")
	local legpos legend(ring(0) position(4) row(2))
	local gopts `glocals' `topts' `legpos' name(cip`cip', replace)

	* save graph in memory
	twoway line ctotalm ctotalw year if cip2 == `cip', `gopts'
}
graph close _all

local cip_top12 : subinstr local top12 " " " cip", all
graph combine cip`cip_top12', rows(4) xcommon








restore





* Want to break down 
* 26: Biological Sciences 
* 52: Business and related services
* 51: Health Professions
* 54: History (is it really that big?)
* 42: Psychology
* 45: Social Sciences







* total men and women over time by two digit cipcode
preserve

gen cip2 = substr(cipcode2010,1,2)
collapse (sum) ctotalm ctotalw, by(cip2 year)



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
