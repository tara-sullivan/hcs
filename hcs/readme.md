I use absolute imports rooted at the root directory (hcs/). to do this, I first
must modify the sys.path. 

To get the current path, I first try using the '__file__' attribute. However, 
this attribute might not work (for instance, it doesn't work when through 
py2exe). If this raises a nameerror, I find the current path using the inspect 
module. 

I then exclusively use absolute imports (even in the same directory). For 
plot_line_labels.py to import tol_colors.py, I need to run:
import img.code.tol_colors

To run a program, I can do any of the following:
* Run as an imported module instead of a script:
    1. Change working directory to root directory (hcs/)
    2. python -m img.code.plot_line_labels
* Run directly as a script
    1. Change working directory to directory with script (cd img/code/)
    2. python plot_line_labels.py
* Interactively run using interpreter
    * SublimeREPL
    * iPython: %run plot_line_labels.py 

hcs/
    img/
        code/
            plot_line_labels.py 
            tol_colors.py
    ipeds/
        plot_n_degreees.py 
        make_df.py


**References**

python imports: https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html

relative imports and inspect module: https://stackoverflow.com/a/11158224

__file__ attribute and py2exe: https://stackoverflow.com/questions/2292703/how-can-i-get-the-executables-current-directory-in-py2exe