The Hack Assembler translates programs written in the Hack assembly language into binary code understood by the Hack computer. The assembler follows the Hack ISA and produces 16-bit binary instructions.

Usage:
The assembler is a single Python script, assembler.py. To use the assembler, follow the steps below:

Step 1: Input File
- Prepare a .asm file containing your Hack assembly code that you want to translate into binary.

Step 2: Running the Assembler
- Open a terminal and navigate to the directory containing the assembler.py script and your .asm file.

--> To see usage details and command-line options, run the following command: $ python assembler.py

--> To create a Hack binary version of your .asm file, run: $ python assembler.py <filename.asm>
** Replace <filename.asm> with the actual name of your .asm file to get the appropriate .hack file.**

Step 3: Output
The assembler will generate a corresponding .hack file that contains the translated binary instructions.



