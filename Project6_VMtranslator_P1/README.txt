This version of a VM translator implements stack arithmetic and memory-access commands by supporting push and pop stack operations from/to the eight memory segments. The translator successfully translates VM commands into corresponding Hack assembly-language commands, which can then be run through an assembler to produce binary code understood by the Hack computer.

Usage:
The VM translator is a single Python script, vm_translator.py. To use the VM translator, follow the steps below:

Step 1: Input File
- Prepare a .vm file containing text lines of VM commands that you want to translate into Hack assembly code.

Step 2: Running the VM translator
- Open a terminal and navigate to the directory containing the vm_translator.py script and your .vm file.

--> To see usage details and command-line options, run the following command: $ Python vm_translator.py

--> To create a Hack assembly code version of your .vm file, run: $ Python vm_translator.py <filename.vm>
** Replace <filename.vm> with the actual name of your .vm file to get the appropriate .asm file.**

Step 3: Output
The VM translator will generate a corresponding .asm file that contains the translated assembly code instructions.
