# Overview of directories

Below is an overview of what is contained in each of the above directories. 
More detailed documentation and replication instructions can be found in any referenced readmes.

### data/

    * ipeds/
        * c/
        * gr/
    * acs/
    
The `/data/ipeds/` directory contains IPEDS data used in this project. 
Two IPEDS surveys are used: completion surveys and graduation surveys.
Replication instructions for the completion surveys can be found in the `data/ipeds/c/`; see the readme in that folder for more information.
Replication instructions for graduation surveys can be found in `data/ipeds/gr/`; see the readme in that folder for more information.

The IPEDS graduation survey directory (in `ipeds/gr/`) and ACS data directory (in `acs/`) only have some exploratory/basic cleaning programs.
I may not use these data in the final version of this project.
For a detailed example of how I structure data tasks, see the IPEDS completion surveys, located in `ipeds/c/`)

### img/

    * code/
    * PGF plots code 

Contains TeX code to generate images used in this project. 
Some commonly referenced code snippeds are in the `img/code/` folder.
I create images for this project by using  [tikzplotlib](https://github.com/nschloe/tikzplotlib) to generate [PGF plots](http://pgfplots.sourceforge.net/) code, which I then compile in TeX. 
The `img/` directory does not contain PDF images, only the code.
To see standalone PDFs used in a particular writeup (either the slides or the paper), navigate to the relevant writeup folder, and click on the figures subfolder. 

### model/

    * afmodel.py
    * beta_distribution_example.py
    * model_plots.py
    * sim_agents.py
    * sim_plots.py

Contains python code for finding optimal policy of agents in a simple version of my model; for simulating agent behavior; and for generating plots about agent characteristics and agent behavior. 

### writeups/

    * paper/
        * figures/
        * outline.tex
        * 01-intro.tex
        * 02-model.tex
        * 03-proof.tex
        * 04-sims.tex
        * 05-stat_discrim.tex
        * a1-solve_index.tex
        * a2-data_resources.tex
        * preamble.tex
        * preamble-outline.tex
        * preamble-figs_bibs.tex
        * bibliography.bib
    * slides/
        * figures/
        * slides.tex
        * preambleB.tex
        * 02-model.tex
        * 03-simulations.tex
        * appendix.tex
        
Contains TeX code for project. 
The main output of this project are the paper itself and the associated slide deck.
Standalone versions of the figures from the paper or slides are found in `paper/figures/` and `paper/slides/`, respectively.
