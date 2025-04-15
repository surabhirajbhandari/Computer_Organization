# -*- coding: utf-8 -*-
"""
Compiler back-end for the Hack processor.
Translates from a stack-based language for the virtual machine to the Hack assembly code.

Adds support for program flow and subroutines.

Author: Naga Kandasamy
Date created: September 1, 2020
Date modified: August 8, 2023


Student names(s): Surabhi Rajbhandari
Date modified: 8/28/23
"""
import os
import sys

line_number = 1
call = 1
addr_map = {'local':'@LCL', 'argument':'@ARG', 'this':'@THIS', 'that':'@THAT', 'pointer':3, 'temp':5, 'static':1024}
arithmetic_logic_map = {'add':'+', 'sub':'-', 'and':'&', 'or':'|', 'not':'!', 'neg':'-'}

def generate_exit_code():
    """Generate epilogue code that places the program, upon completion, into 
    an infinite loop. 
    """
    s = []
    s.append('(THATS_ALL_FOLKS)')
    s.append('@THATS_ALL_FOLKS')
    s.append('0;JMP')
    return s


def generate_push_code(segment, index):
    """Generate assembly code to push value into the stack.
    In the case of a variable, it is read from the specified memory segment using (base + index) 
    addressing.
    """
    s = [] 
        
    if segment == 'constant':
        # FIXME: complete the implementation 
        s.append('@{}'.format(index))
        s.append('D=A')
    else:
        # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
        if segment in ('local', 'argument', 'this', 'that'):
            s.append(addr_map.get(segment))
            s.append('D=M')
            s.append('@{}'.format(index))
            s.append('A=D+A')        
            s.append('D=M')     
        elif segment in ('temp','pointer'):
            s.append('@R{}'.format(addr_map.get(segment) + int(index)))
            s.append('D=M')
        elif segment == 'static':
            s.append('@{}'.format(addr_map.get(segment) + int(index)))
            s.append('D=M')

    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')    
    
    return s
    
def generate_pop_code(segment, index):
    """Generate assembly code to pop value from the stack.
    The popped value is stored in the specified memory segment using (base + index) 
    addressing.
    """
    s = []
    if segment in ('local', 'argument', 'this', 'that'):
        s.append(addr_map.get(segment))
        s.append('D=M')
        s.append('@{}'.format(index))
        s.append('D=D+A')
    elif segment in ('temp','pointer'):
        s.append('@R{}'.format(addr_map.get(segment) + int(index)))
        s.append('D=A')
    elif segment == 'static':
        s.append('@{}'.format(addr_map.get(segment) + int(index)))
        s.append('D=A')
    else:
        print('Invalid pop, segment: {}'.format(segment))
    
    s.append('@R13')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@R13')
    s.append('A=M')
    s.append('M=D')
    
    return s

def generate_arithmetic_or_logic_code(operation):
    """Generate assembly code to perform specified ALU operation. 
    The two operands are popped from the stack and result of operation 
    pushed back in the stack.
    """
    s = []

    if operation in ('add','sub','and','or'):
        # FIXME: complete implementation for + , - , | , and & operators
        s.append('@SP')
        s.append('M=M-1')
        s.append('A=M')
        s.append('D=M')
        s.append('@SP')
        s.append('M=M-1')
        s.append('A=M')
        s.append('D=M{}D'.format(arithmetic_logic_map.get(operation)))
        s.append('@SP')
        s.append('A=M')
        s.append('M=D')
        s.append('@SP')
        s.append('M=M+1')

    return s

def generate_unary_operation_code(operation):
    """Generate assembly code to perform specified unary operation. 
    The operand is popped from the stack and result of operation 
    pushed back in the stack.
    """
    s = []
    
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M={}D'.format(arithmetic_logic_map.get(operation)))
    s.append('@SP')
    s.append('M=M+1')
    
    return s

def generate_relation_code(operation, line_number):
    """Generate assembly code to perform the specified relational operation. 
    The two operands are popped from the stack and result of the operation 
    pushed back in the stack.
    """
    s = []
    label_1 = ''
    label_2 = ''
    
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')             # D  = operand2
    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer
    s.append('A=M')
        
    if operation == 'lt':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_LT_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JLT')       # if operand1 < operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Save result on stack 
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Save result on stack
        s.append('(' + label_2 + ')')
    elif operation == 'eq':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_EQ_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JEQ')       # if operand1 = operand2 goto IF_EQ_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Save result on stack 
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Save result on stack
        s.append('(' + label_2 + ')')
    elif operation == 'gt':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_GT_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JGT')       # if operand1 > operand2 goto IF_GT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Save result on stack 
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Save result on stack
        s.append('(' + label_2 + ')')
        
    s.append('@SP')
    s.append('M=M+1')

    return s
  

def generate_if_goto_code(label):
    """Generate code for the if-goto statement. 

    Behavior:
    
    1. Pop result of expression from stack.
    2. If result is non-zero, goto LABEL.
    
    """
    s = []
    
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@{}'.format(label))
    s.append('D;JNE')
    
    return s

def generate_goto_code(label):
    """Generate assembly code for goto."""
    s = []
    
    s.append('@{}'.format(label))
    s.append('0;JMP')
    
    return s

def generate_pseudo_instruction_code(label):   
    """Generate pseudo-instruction for label."""
    s = []
    
    s.append('(' + label + ')')
    return s

def generate_set_code(register, value):
    """Generate assembly code for set"""
    s = []
    
    s.append('@' + value)
    s.append('D=A')
    
    if register == 'sp':
        s.append('@SP')
    
    if register == 'local':
        s.append('@LCL')
    
    if register == 'argument':
        s.append('@ARG')
        
    if register == 'this':
        s.append('@THIS')
        
    if register == 'that':
        s.append('@THAT')
        
    s.append('M=D')
    
    return s

def generate_function_call_code(function, nargs, line_number):  
    global call
    """Generate preamble for function"""
    s = []
    
    # Push return address to stack
    s.append('@{}_label_{}'.format(function, call))
    s.append('D=A')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')  
    # Push LCL, ARG, THIS, and THAT registers to stack
    s.append('@LCL')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')  

    s.append('@ARG')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')  
    
    s.append('@THIS')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')  
    
    s.append('@THAT')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')  

    # Set ARG register to point to start of arguments in the current frame, ARG = SP - n - 5
    s.append('@SP')
    s.append('D=M')
    s.append('@5')
    s.append('D=D-A')
    s.append('@{}'.format(nargs))
    s.append('D=D-A')
    s.append('@ARG')
    s.append('M=D')

    # Set LCL register to current SP
    s.append('@SP')
    s.append('D=M')
    s.append('@LCL')
    s.append('M=D')
    
    # Generate goto code to jump to function
    s.append('@{}'.format(function))
    s.append('0;JMP')
    
    # Generate the pseudo-instruction/label corresponding to the return address
    s.append('({}_label_{})'.format(function, call))
    call+=1
    
    return s

def generate_function_body_code(f, nvars):
    """Generate code for function f.
    f: name of the function, which should be located in a separate file called f.vm
    nvars: number of local variables declared within the function.
    """
    s = []
    
    # Generate the pseudo instruction -- the label
    s.append('({})'.format(f))

    # FIXME: Push nvars local variables into the stack, each intialized to zero
    s.append('@i')
    s.append('M=0')
    s.append('@{}'.format(nvars))
    s.append('D=A')
    s.append('@n')
    s.append('M=D')

    # while i < n:
    s.append('({}_WHILE_LOOP)'.format(f))
    s.append('@n')
    s.append('D=M')
    s.append('@i')
    s.append('D=D-M')
    s.append('@{}_END_WHILE_LOOP'.format(f))
    s.append('D;JEQ') # jump to end when i = n

    # initialize 0
    s.append('@SP')
    s.append('A=M')
    s.append('M=0')

    # i++ and SP++
    s.append('@i')
    s.append('M=M+1')
    s.append('@SP')
    s.append('M=M+1')

    # jump back to start of loop
    s.append('@{}_WHILE_LOOP'.format(f))
    s.append('0;JMP')

    # end loop label
    s.append('({}_END_WHILE_LOOP)'.format(f))
    
    return s


def generate_function_return_code():
    """Generate assembly code for function return"""
    s = []
    
    s.append('// Copy LCL to temp register R14 (FRAME)')
    # Copy LCL to temp register R14 (FRAME)
    s.append('@LCL')
    s.append('D=M')
    s.append('@R14')
    s.append('M=D')
    
    s.append('// Store return address in temp register R15 (RET)')
    # Store return address in temp register R15 (RET)
    s.append('@R14')
    s.append('D=M')
    s.append('@5')
    s.append('A=D-A')
    s.append('D=M')
    s.append('@R15')
    s.append('M=D')
    
    s.append('// Pop result from the working stack and move it to beginning of ARG segment')
    # Pop result from the working stack and move it to beginning of ARG segment
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@ARG')
    s.append('A=M')
    s.append('M=D')

    # Adjust SP = ARG + 1
    s.append('@ARG')
    s.append('D=M+1')
    s.append('@SP')
    s.append('M=D')
    
    # Restore THAT = *(FRAME - 1)
    s.append('@R14')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@THAT')
    s.append('M=D')
    
    # Restore THIS = *(FRAME - 2)
    s.append('@R14')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@THIS')
    s.append('M=D')
   
    
    # Restore ARG = *(FRAME - 3)
    s.append('@R14')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@ARG')
    s.append('M=D')
    
    
    # Restore LCL = *(FRAME - 4)
    s.append('@R14')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')
    s.append('@LCL')
    s.append('M=D')    
    
    # Jump to return address stored in R15 back to the caller code
    s.append('@R15')
    s.append('A=M')
    s.append('0;JMP')
   
    return s

def translate_vm_commands(tokens, line_number):
    """Translate a VM command into corresponding Hack assembly commands."""
    s = []
    
    if tokens[0] == 'push':
        s = generate_push_code(tokens[1], tokens[2])    # Generate code to push into stack
        
    elif tokens[0] == 'pop':
        s = generate_pop_code(tokens[1], tokens[2])     # Generate code to pop from stack
        
    elif tokens[0] == 'add' or tokens[0] == 'sub' \
         or tokens[0] == 'or' or tokens[0] == 'and':
        s = generate_arithmetic_or_logic_code(tokens[0])  # Generate code for ALU operation
        
    elif tokens[0] == 'neg' or tokens[0] == 'not':
        s = generate_unary_operation_code(tokens[0])    # Generate code for unary operations
        
    elif tokens[0] == 'eq' or tokens[0] == 'lt' or tokens[0] == 'gt':
        s = generate_relation_code(tokens[0], line_number)
    
    elif tokens[0] == 'label':
        s = generate_pseudo_instruction_code(tokens[1])
    
    elif tokens[0] == 'if-goto':
        s = generate_if_goto_code(tokens[1]) 
        
    elif tokens[0] == 'goto':
        s = generate_goto_code(tokens[1])
    
    elif tokens[0] == 'end':
        s = generate_exit_code()
        
    elif tokens[0] == 'set':
        s = generate_set_code(tokens[1], tokens[2])
        
    elif tokens[0] == 'function':
        s = generate_function_body_code(tokens[1], int(tokens[2]))
        
    elif tokens[0] == 'call':
        s = generate_function_call_code(tokens[1], tokens[2], line_number)
        
    elif tokens[0] == 'return':
        s = generate_function_return_code()
        
    else:
        print('translate_vm_commands: Unknown operation')           # Unknown operation 
    
    return s
    
def translate_file(input_file):
    """Translate VM file to Hack assembly code"""
    global line_number
    assembly_code = []
    assembly_code.append('// ' + input_file)
    
    with open(input_file, 'r') as f:
        for command in f:        
            # print("Translating line:", line_number, command)
            tokens = (command.rstrip('\n')).split()
            
            if not tokens:
                continue                                        # Ignore blank lines  
            
            if tokens[0] == '//':
                continue                                        # Ignore comment       
            else:
                s = translate_vm_commands(tokens, line_number)
                line_number = line_number + 1        
            if s:
                
                for i in s:
                    assembly_code.append(i)
            else:
                return False
            
    # Write translated commands to .i file
    file_name_minus_extension, _ = os.path.splitext(input_file)
    output_file = file_name_minus_extension + '.i'
    out = open(output_file, 'w')
    for s in assembly_code:
        out.write('%s\n' %s)
    out.close()
    print('Assembly file generated: ', output_file)
        
    return True

def run_vm_to_asm_translator(path):
    """Main translator code"""
    files = os.listdir(path)
    
    cwd = os.getcwd()
    os.chdir(path)
    
    if 'sys.vm' in files:
        idx = files.index('sys.vm')
        f = files.pop(idx)
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    else:
        print('Missing sys.vm file')
        return False
        
    if 'main.vm' in files:
        idx = files.index('main.vm')
        f = files.pop(idx)
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    else:
        print('Missing main.vm file')
        return False
    
    for f in files:
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    
    os.chdir(cwd)
    
    return True

def assemble_final_file(output_file, path):
    """Assemble final output file"""
    intermediate_files = []
    files = os.listdir(path)
    for f in files:
        if f.endswith('.i'):
            intermediate_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    with open(output_file, 'w') as outfile:    
        idx = intermediate_files.index('sys.i')
        f = intermediate_files.pop(idx)
        with open(f, 'r') as infile:
            for line in infile:
                outfile.write(line)
        
        idx = intermediate_files.index('main.i')
        f = intermediate_files.pop(idx)
        with open(f, 'r') as infile:
            for line in infile:
                outfile.write(line)
        
        for f in intermediate_files:
            with open(f, 'r') as infile:
                for line in infile:
                    outfile.write(line)

    os.chdir(cwd)
    return True
    
def clean_intermediate_files(path):
    """Removes intermediate .i files from supplied path"""
    intermediate_files = []
    
    files = os.listdir(path)
    for f in files:
        if f.endswith('.i'):
            intermediate_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    for f in intermediate_files:
        os.remove(f)
    
    os.chdir(cwd)
        

def clean_old_files(path):
    """Removes old files from supplied path"""
    old_files = []
    
    files = os.listdir(path)
    for f in files:
        if f.endswith('.asm') or f.endswith('.i') or f.endswith('.hack'):
            old_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    for f in old_files:
        os.remove(f)
    
    os.chdir(cwd)
    
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: Python vm_translator_v2.py file-name.asm path-name")
        print("file-name.asm: assembly file to be generated by the translator")
        print("path-name: directory containing .vm source files")
        print("Example: Python vm_translator_v2.py mult-final.asm ./mult")
    else:
        output_file = sys.argv[1]
        path = sys.argv[2]
        clean_old_files(path)
        
        status = run_vm_to_asm_translator(path)
        if status == True:
            print('Intermediate assembly files were generated successfully');
            print('Generating final assembly file: ', output_file)
            assemble_final_file(output_file, path)
            # clean_intermediate_files(path)
        else:
            print('Error generating assembly code')