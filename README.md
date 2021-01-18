# Group-based beliefs and Human Capital Specialization 

This folder contains replication code for my job market paper. 
The primary output for this project are PDFs generated in TeX, specifically my slides (`hcs/writeups/slides/slides.pdf`) and my paper (`hcs/writeups/paper/outline.pdf`). 
To generate these PDFs, I compile  `hcs/writeups/slides/slides.tex` and `hcs/writeups/paper/outline.tex`, respectively.

## Replication notes

### Data paths to update

This project utilizes several large datasets. 
In order for this code to be run locally, several data paths need to be changed:
* The path to raw IPEDs completion surveys in `data/ipeds/c/clean_data/ipeds_cip_merge.do` and `data/ipeds/c/clean_data/ipeds_c_clean.do`
* The path to raw IPEDS graduation surveys in `data/ipeds/gr/ipeds_gr_clean.py`
* The path to raw ACS data in `data/acs/make_acs_df.py`

For more details, see the readme's in each of the respective data folders.

### Running code

I use [tikzplotlib](https://github.com/nschloe/tikzplotlib) to generate [PGFPlots](http://pgfplots.sourceforge.net/) code for this project.
Therefore, you must run TeX to generate PDF figures. 
To generate standalone versions of figures (and to make my TeX code compile faster), externalize the PGFPlots figures.
This means that when I compile my tex, code, I run the following commands:
```shell session
cd witeups/paper
pdflatex -shell-escape sullivan[2020]-jmp
```
The resulting pdfs can be found in the relevant `figures/` subfoler. 

### System path and imports

Most of the python code in this repository starts by finding the root directory, `hcs/hcs/`, and adding it to the path.
I first try to find the current directory using the `__file__` attribute.
If this attribute [does not work](https://stackoverflow.com/questions/2292703/how-can-i-get-the-executables-current-directory-in-py2exe) and raises a nameerror (which happens when running interactively), I find the current path using the [inspect module](https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder/11158224#11158224). 
I then add the root directory to the path.
When importing other modules, I use [absolute imports](https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html#absolute-vs-relative-import) beginning at the root directory.

To run a program like `plot_line_labels.py` (located in `hcs/hcs/img/code`), I can do any of the following:
* Run as an imported module instead of a script:
    1. Change working directory to root directory (`hcs/hcs/`)
    2. `python -m img.code.plot_line_labels`
* Run directly as a script
    1. Change working directory to directory with script (cd `img/code/`)
    2. `python plot_line_labels.py`
* Interactively run using interpreter
    * SublimeREPL
    * iPython: `%run plot_line_labels.py`

I do this using the following code:
```python
# Handle file paths; set root directory
import os
import sys
import inspect
try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(currpath))
sys.path.append(rootdir)
```
Note that I might need to edit the `rootdir` variable, depending on the location of this particular program (this one is located in `hcs/hcs/model/').

There are other ways to do this, but this works best for my workflow. 
My preferred text editor is [Sublime Text 3](https://www.sublimetext.com/3). 
When developing code, I often run an interpreter inside Sublime Text using the [SublimeREPL package](https://packagecontrol.io/packages/SublimeREPL).
I also often run modules from the command line or in bash scripts. 
Including the above preamble allows me to jump between all of these methods.
It does mean that I need to manually change the preamble whenever I change my file structure (though if there's a better way to do this, please let me know!)
