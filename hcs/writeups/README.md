# Overview of `/writeups/`

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


The primary output for this project are PDFs generated in TeX, specifically my slides (`hcs/writeups/slides/slides.pdf`) and my paper (`hcs/writeups/paper/outline.pdf`). 
To generate these PDFs, I compile  `hcs/writeups/slides/slides.tex` and `hcs/writeups/paper/outline.tex`, respectively (henceforth `slides.tex` and `outline.tex`).

The TeX root file for my paper is `paper/outline.tex`. 
The TeX preamble commands are defined in `paper/preamble.tex`, `paper/preamble-outline.tex`, and `paper/preamble-figs_bibs.tex`.
Subfiles begining with a number (e.g. `paper/01-intro.tex`, `paper/02-model.tex`, etc.) comprise the body of the text. 
Subfiles beginning with the letter `a` and a number (e.g. `paper/a1-solve_index.tex`) comprise the appendix.

The TeX root file for my slides is `slides/slides.tex`. The TeX preamble commands are defined in `slides/preambleB.tex`. 
Subfiles beginning with a number (e.g. `slides/02-model.tex`, etc.) comprise the body of the presentation. 
The subfile `appendix.tex` contains appendix slides. 

## Standalone figures

Standalone versions of the figures from the paper or slides are found in the directories `paper/figures/` and `slides/figures`, respectively.

These PDFs contain figures generated using programs from my `model/` and `data/` directories.
I generate these figures in Python using matplotlib, but need to save them in a TeX-friendly way.
To do this, I convert my matplotlib lib code to TeX code using  [tikzplotlib](https://github.com/nschloe/tikzplotlib). 
That way, I can natively compile my figures in TeX using [PGF plots](http://pgfplots.sourceforge.net/).

To generate standalone versions of figures (and to make my TeX code compile faster), externalize the PGFPlots figures.
This means that when I compile my tex, code, I run the following commands:
```shell
cd witeups/paper
pdflatex -shell-escape slides
```
The resulting pdfs can be found in the relevant `figures/` sub-directory.

## Bibliographic information

The bibliography is defined in `bibliography.bib`. I use Biblatex with a Biber backend to create my bibliography.
To properly compile this bibliography, one must run something like: 
```shell
pdflatex outline.tex
pdflatex outline.tex
biber outline
pdflatex outline.tex
```
I recommend automating this process using a batch file. 

## Compiling TeX documents

I use [tikzplotlib](https://github.com/nschloe/tikzplotlib) to generate [PGFPlots](http://pgfplots.sourceforge.net/) code for this project.
Therefore, you must run TeX to generate PDF figures. 
To generate standalone versions of figures (and to make my TeX code compile faster), externalize the PGFPlots figures in my 
This means that when I compile my tex, code, I run the following commands:
```shell session
cd witeups/paper
pdflatex -shell-escape sullivan[2020]-jmp
```
The resulting pdfs can be found in the relevant `figures/` subfoler. 
