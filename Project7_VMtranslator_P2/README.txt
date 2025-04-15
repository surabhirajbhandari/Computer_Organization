This version of a VM translator extends the previous build by adding support for program-flow commands and subroutines. This VM translator can handle if-goto and goto commands for conditional and unconditional jumps, as well as function-related commands such as 'function f k', 'call f n', and 'return'. The translator successfully converts VM commands into corresponding Hack assembly-language commands, which can then be run through an assembler to produce binary code understood by the Hack computer.

Usage:
The VM translator is a single Python script, vm_translator_v2.py. To use the VM translator, follow the steps below:

Step 1: Input Files and Directory
- Prepare a folder in the same directory as the Python script that contains all of the .vm files for a program. Each of the files will be translated into Hack assembly code and then combined into a single .asm file that can be fed to the assembler. Ensure that the files 'sys.vm' and 'main.vm' are included for the initialization routine and entry point into the program, respectively. Any additional files that contain related VM function commands can also be placed in this directory. 

Step 2: Running the VM translator
- Open a terminal and navigate to the directory containing the vm_translator_v2.py script and your .vm source files.

--> To see usage details and command-line options, run the following command: $ Python vm_translator_v2.py

--> To create a Hack assembly code version of your .vm files, run: $ Python vm_translator_v2.py <filename.asm> <path-name>
** Replace <filename.asm> with the intended output name for the combined .asm file.**
** Replace <path-name> with the name of the directory containing the .vm source files.**

Example: $ Python vm_translator_v2.py add-final.asm ./add 
- The command line arguments for a simple addition program that has the .vm source files in a folder named 'add'.
	 
Step 3: Output
The VM translator will generate a corresponding .asm file in the same directory that contains all of the translated assembly code instructions.



