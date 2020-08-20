# Overview of directories

Below is an overview of what is contained in each of the above directories. 
More detailed documentation and replication instructions can be found in any referenced readmes.

### data/

* data/
    * ipeds/
        * c
        * gr
    * acs/
    
The `/data/ipeds/` directory contains IPEDS data used in this project. 
Two IPEDS surveys are used: completion surveys and graduation surveys.
Replication instructions for the completion surveys can be found in the `data/ipeds/c/`; see the readme in that folder for more information.
Replication instructions for graduation surveys can be found in `data/ipeds/gr/`; see the readme in that folder for more information.

### img/

* img/
    * code/
    * PGF plots code 

Contains TeX code to generate images used in this project. 
Some commonly referenced code snippeds are in the `img/code/` folder.
I create images for this project by using  [tikzplotlib](https://github.com/nschloe/tikzplotlib) to generate [PGF plots](http://pgfplots.sourceforge.net/) code, which I then compile in TeX. 
The `img/` directory does not contain PDF images, only the code.
To see standalone PDFs used in a particular writeup (either the slides or the paper), navigate to the relevant writeup folder, and click on the figures subfolder. 

### model/

### writeups/

* writeups/
    * paper/
        * sullivan[2020]-jmp.tex
        * preamble.tex
        * preamble-outline.tex
        * figures/
    * slides/
        * slides.tex
        * preambleB.tex
        * 02-model.tex
        * 03-simulations.tex
        * figures/
    * bibliography.bib

Contains TeX code for project. 
The main output of this project are the paper itself and the associated slide deck.
Standalone versions of the figures from the paper or slides are found in `paper/figures/` and `paper/slides/`, respectively.
