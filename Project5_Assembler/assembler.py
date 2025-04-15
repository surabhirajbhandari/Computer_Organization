# -*- coding: utf-8 -*-
"""Assembler for the Hack processor.

Author: Naga Kandasamy
Date created: August 8, 2020
Date modified: July 24, 2023

Student name(s): Surabhi Rajbhandari
Date modified: 08/15/23
"""

import os
import sys

rom_address = 0
ram_address = 16

"""The comp field is a c1 c2 c3 c4 c5 c6"""
valid_comp_patterns = {'0':'0101010', 
                       '1':'0111111',
                       '-1':'0111010',
                       'D':'0001100',
                       'A':'0110000',
                       '!D':'0001101',
                       '!A':'0110001',
                       '-D':'0001111',
                       '-A':'0110011',
                       'D+1':'0011111',
                       'A+1':'0110111',
                       'D-1':'0001110',
                       'A-1':'0110010',
                       'D+A':'0000010',
                       'D-A':'0010011',
                       'A-D':'0000111',
                       'D&A':'0000000',
                       'D|A':'0010101',
                       'M':'1110000',
                       '!M':'1110001',
                       '-M':'1110011',
                       'M+1':'1110111',
                       'M-1':'1110010',
                       'D+M':'1000010',
                       'M+D':'1000010',
                       'D-M':'1010011',
                       'M-D':'1000111',
                       'D&M':'1000000',
                       'D|M':'1010101'
                       }

"""The dest bits are d1 d2 d3"""
valid_dest_patterns = {'null':'000',
                       'M':'001',
                       'D':'010',
                       'MD':'011',
                       'A':'100',
                       'AM':'101',
                       'AD':'110',
                       'AMD':'111'
                       }

"""The jump fields are j1 j2 j3"""
valid_jmp_patterns =  {'null':'000',
                       'JGT':'001',
                       'JEQ':'010',
                       'JGE':'011',
                       'JLT':'100',
                       'JNE':'101',
                       'JLE':'110',
                       'JMP':'111'
                       }

"""Symbol table populated with predefined symbols and RAM locations"""
symbol_table = {'SP':0,
                'LCL':1,
                'ARG':2,
                'THIS':3,
                'THAT':4,
                'R0':0,
                'R1':1,
                'R2':2,
                'R3':3,
                'R4':4,
                'R5':5,
                'R6':6,
                'R7':7,
                'R8':8,
                'R9':9,
                'R10':10,
                'R11':11,
                'R12':12,
                'R13':13,
                'R14':14,
                'R15':15,
                'SCREEN':16384,
                'KBD':24576
                }

def print_intermediate_representation(ir):
    """Print intermediate representation"""
    
    for i in ir:
        print()
        for key, value in i.items():
            print(key, ':', value)

        
def print_instruction_fields(s):
    """Print fields in instruction"""
    
    print()
    for key, value in s.items():
        print(key, ':', value)


def valid_tokens(s):
    """Return True if tokens belong to valid instruction-field patterns"""
    if (s['comp'] in valid_comp_patterns) and (s['dest'] in valid_dest_patterns) and (s['jmp'] in valid_jmp_patterns):
        return True
    
    if s['instruction_type'] == 'A-INSTRUCTION':
        return True

def parse(command):
    """Implements finite automate to scan hack assembly commands and parse them.

    WHITE SPACE: Space characters are ignored. Empty lines are ignored.
    
    COMMENT: Text beginning with two slashes (//) and ending at the end of the line is considered 
    comment and is ignored.
    
    CONSTANTS: Must be non-negative and are written in decimal notation. 
    
    SYMBOL: A user-defined symbol can be any sequence of letters, digits, underscore (_), dot (.), 
    dollar sign ($), and colon (:) that does not begin with a digit.
    
    LABEL: (SYMBOL)
    """
    global rom_address
    command = command.strip()
    command = command.replace(' ','')
    command = command.replace('\n','')
    print(command)
    
    # Data structure to hold the parsed fields for the command
    s = {}
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0
      
    
    # Valid operands and operations for C-type instructions
    valid_operands = '01DMA'
    valid_operations = '+-&|'

    if not command or command.startswith('//'):
        return None
    
    
    if command.startswith('(') and command.endswith(')'):
        s['instruction_type'] = 'PSEUDO_INSTRUCTION'
        s['value'] = command[1:-1]
        symbol_table[s['value']] = rom_address
    
    elif command.startswith('@'):
            rom_address+=1
            s['instruction_type'] = 'A-INSTRUCTION'
            s['value'] = command[1:]
            s['comp'] = ''
            
            if command[1:].isdigit():
                s['value_type'] = 'NUMERIC'
                s['dest'] = 'null'
                s['jmp'] = 'null'

            else:
                s['value_type'] = 'SYMBOL'
                s['dest'] = ''
                s['jmp'] = ''
    else:
            rom_address+=1
            s['instruction_type'] = 'C-INSTRUCTION'

            if '=' in command:
                command = command.replace('//','=')

                comps = command.split('=')
                s['dest'] = comps[0]
                s['comp'] = comps[1]
                s['jmp'] = 'null'

            elif ';' in command:
                command = command.replace('//',';')

                comps = command.split(';')
                print(comps)
                s['dest'] = 'null'
                s['comp'] = comps[0]
                s['jmp'] = comps[1]
    
    
    # FIXME: Implement your finite automata to extract tokens from command
    for char in command:
        pass
    
    # FIXME: check if the tokens were formed correctly
    if valid_tokens(s):
        return s
    return None   
   
def generate_machine_code():
    """Generate machine code from intermediate data structure"""
    
    global ram_address
    #print('IN GEN MACH CODE')
    #print(s)

    instruction = ''
    if s['instruction_type'] == 'A-INSTRUCTION':
        print('A')

        instruction += '0'
        if s['value_type'] == 'NUMERIC':
            #instruction = instruction 
            instruction = instruction + format(int(s['value']), 'b').zfill(15)

        elif s['value_type'] == 'SYMBOL':
            if s['value'] in symbol_table:
                var_address = symbol_table[s['value']]
                instruction = instruction + format(var_address, 'b').zfill(15)
            else:
            # Insert entry into table
                symbol_table[s['value']] = ram_address
                instruction = instruction + format(ram_address, 'b').zfill(15)
                ram_address = ram_address + 1
        else:
            pass


    elif s['instruction_type'] == 'C-INSTRUCTION':
        print('C')
        instruction += '111'
        instruction = instruction + valid_comp_patterns[s['comp']]
        instruction = instruction + valid_dest_patterns[s['dest']]
        instruction = instruction + valid_jmp_patterns[s['jmp']]
    
    else:
        print('ELSE')
        pass
        
    
    
    return instruction
    

def print_machine_code(machine_code):
    """Print generated machine code"""
    
    rom_address = 0
    for code in machine_code:
        print(rom_address, ':', code)
        rom_address = rom_address + 1


def run_assembler(file_name):      
    """Pass 1: Parse the assembly commands into an intermediate data structure.
    This can be a list of elements, called ir, where each element is a dictionary with the following 
    structure: 
    
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0
    
    The symbol table is also generated in this step.    
    """
    ram_address = 1024
    # FIXME: Implement Pass 1 of the assembler to generate the intermediate data structures
    ir_structs = [] 
    with open(file_name, 'r') as f:
        for command in f:  
            s = parse(command)
            print(s)
            if s != None:
                ir_structs.append(s)
    
    
    # FIXME: Implement Pass 2 of assembler to generate the machine code from the intermediate data structures
    machine_code = []
    for i in ir_structs:
        instr = generate_machine_code(i)
        machine_code.append(instr)

    print(len(machine_code))
    print_machine_code(machine_code)
        
    return machine_code
    
  
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python assembler.py file-name.asm")
        print("Example: Python assembler.py series_sum.asm")
    else:
        print("Assembling file:", sys.argv[1])
        print()
        file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
        output_file = file_name_minus_extension + '.hack'
        machine_code = run_assembler(sys.argv[1])
        if machine_code:
            print('Machine code was generated successfully');
            print('Writing machine code output to file:', output_file)
            f = open(output_file, 'w')
            for s in machine_code:
                f.write('%s\n' %s)
            f.close()
        else:
            print('Error generating machine code')
            
        

    
    
    
    
