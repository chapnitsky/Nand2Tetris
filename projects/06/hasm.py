#!/usr/bin/python3
# Some text copyright (C) 2011 Mark Armbrust.  
# Permission granted for educational use.
# Skeletonized March 2016 by Janet Davis
# Refactored May 2016 by Janet Davis
# Refactored February 2018 by John Stratton
# Refactored and debugged January 2019 by Janet Davis

"""
hasm.py -- Hack computer assembler

Translates a Hack assembly program into the corresponding Hack machine language program.
See "The Elements of Computing Systems", by Noam Nisan and Shimon Schocken

Usage: python3 hasm.py PROGRAM.asm
"""

from hasmUtils import *
from sys import argv
import string
import re

def read_asm_file(input_filename):
    """
    Reads the list of assembly commands from input, removing comments.
    Returns a list of non-empty, non-comment lines.  Each should represent 
    a single command, either an A_COMMAND, C_COMMAND, or L_COMMAND
    """
    try:
        inFile = open(input_filename, 'r')
    except:
        FatalError('Could not open source file "'+input_filename+'"')

    rawline = inFile.readline()
    list_of_lines = []

    while rawline != '':
        # Parse the line. Start by removing whitespace
        line = rawline.strip()

        # Then deal with comments
        comment_start = line.find("//")
        if comment_start >= 0:
            # Keep the part of the line before the comment, less whitespace
            line = line[:comment_start].strip()

        # If the entire line is a comment or empty, 
        # do nothing and skip to the next line
        # Otherwise, add the non-empty preprocessed line to the list
        if line != '':
            list_of_lines.append( line )
        rawline = inFile.readline()

    inFile.close()
    return list_of_lines

def command_type(command):
    """
    Returns one of the defined constants A_COMMAND, C_COMMAND, or L_COMMAND 
    to identify the type of command represented by the parameter string.
    If the command is none of these types, throw a FatalError exception.
    """
    # TODO Stage A: Categorize A_COMMAND and C_COMMAND
    # TODO Stage B: Categorize L_COMMAND
    pass

def emit_C_instruction(command, output_file):
    """
    Given an assembly language command corresponding to a C-instruction,
    writes the corresponding machine language instruction to the given output
    file.  The machine langauge instruction should be expressed as a string of 
    16 characters "0" and "1". Each line of the output file should consist
    of exactly one machine language instruction.
    """

    # The CodeTranslator class, defined in hasmUtils.py, has methods 
    # dest(string), comp(string), and jump(string) 
    # to translate assembly mnemonics of each type into strings of 0 and 1.
    codeTranslator = Code()

    # TODO Stage A: translate C command to machine instruction and write to file
    pass

def emit_A_instruction(command, symbol_table, output_file):
    """
    Given an assembly language command corresponding to an A-instruction,
    writes the corresponding machine language instruction to the given output
    file.  The machine langauge instruction should be expressed as a string of 
    16 characters "0" and "1". Each line of the output file should consist
    of exactly one machine language instruction.
    """

    # TODO Stage A: translate C command to machine instruction and write to file
    # TODO Stage B: revise to handle labels as well as integer constants
    pass

def first_pass(command_list, symbol_table):
    """
    Given a list of commands, adds labels to the given symbol table.
    """
    # TODO Stage B: Add labels to symbol table
    pass

def second_pass(command_list, symbol_table, output_filename):
    """
    Translates the given list of commands into a machine language program
    using the given symbol table. The program is written to a file 
    with the given name.
    """

    # Open output file
    output_file = open(output_filename, "w");
    if not output_file:
        FatalError("Cannot open output file " + output_filename)

    # Parse input file and emit code
    for command in command_list:
        if command_type(command) == A_COMMAND:
            emit_A_instruction(command, symbol_table, output_file)
        elif command_type(command) == C_COMMAND:
            emit_C_instruction(command, output_file)
        # Note that we do not emit instructions for label commands

    output_file.close()
   
def main():
    # Get input and output filenames
    input_filename = argv[1]
    match = re.match('^(.*)\.asm$', input_filename)
    if not match:
        FatalError(input_filename + " is not an asm file")
    output_filename = match.groups()[0] + ".hack"

    # Create a symbol table with predefined symbols
    symbol_table = init_symbol_table()

    # Read and preprocess the assembly source code into a list of commands
    list_of_commands = read_asm_file(input_filename)

    # Assemble the code!
    first_pass(list_of_commands, symbol_table)
    second_pass(list_of_commands, symbol_table, output_filename)

if __name__ == '__main__':
    main();
