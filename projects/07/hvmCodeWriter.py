"""
hvmCodeWriter.py -- Emits assembly language code for the Hack VM translator.
Skeletonized by Janet Davis March 2016
Refactored by John Stratton April 2017
Refactored by Janet Davis March 2019
"""

import os
from hvmCommands import *

# If debug is True, 
# then the VM commands will be written as comments into the output ASM file.
debug = True

class CodeWriter(object):
    
    def __init__(self, outputName):
        """
        Opens 'outputName' and gets ready to write it.
        """
        self.file = open(outputName, 'w')
        self.fileName = self.setFileName(outputName)
        self.rand = 0
        # used to generate unique labels
        self.labelNumber = 0
        self.functionName = ""

    def close(self):
        """
        Writes the terminal loop and closes the output file.
        """
        label = self._uniqueLabel()
        self._writeComment("Infinite loop")
        self._writeCode('(%s), @%s, 0;JMP' % (label, label))
        self.file.close()

    def setFileName(self, fileName):
        """
        Sets the current file name to 'fileName'.
        Restarts the local label counter.

        Strips the path and extension.  The resulting name must be a
        legal Hack Assembler identifier.
        """
        self.fileName = os.path.basename(fileName)
        self.fileName = os.path.splitext(self.fileName)[0]

    def _uniqueLabel(self):
        self.labelNumber += 1
        return "label" + str(self.labelNumber)

    def write(self, text):
        """ 
        Write directly to the file.
        """
        self.file.write(text)

    def _writeCode(self, code):
        """
        Writes Hack assembly code to the output file.
        code should be a string containing ASM commands separated by commas,
        e.g., "@10, D=D+A, @0, M=D"
        """
        code = code.replace(',', '\n').replace(' ', '')
        self.file.write(code + '\n')

    def _writeComment(self, comment):
        """
        Writes a comment to the output ASM file.
        """
        if (debug):
            self.file.write('    // %s\n' % comment)

    def _D2Stack(self):
        """
        Writes Hack assembly code to push the value from the D register 
        onto the stack.
        TODO - Stage I - see Figure 7.2
        """
        self._writeCode('@SP, A=M, M=D, @SP, M=M+1') #  'RAM[0] = RAM[0] + 1' = SP++
    
    def _Stack2D(self):
        """"
        Writes Hack assembly code to pop a value from the stack 
        into the D register.
        TODO - Stage I - see Figure 7.2
        """
        self._writeCode('@SP, M=M-1, @SP, A=M, D=M') # D = RAM[SP]

    def writeArithmetic(self, command):
        """
        Writes Hack assembly code for the given command.
        TODO - Stage I - see Figure 7.5
        """
        self._writeComment(command)
        self.rand += 1
        correct_label = f'(Correct{str(self.rand)})'
        correct_load = f'@Correct{str(self.rand)}'

        continue_label = f'(Continue{str(self.rand)})'
        continue_load = f'@Continue{str(self.rand)}'

        notcor_label = f'(NotCorrect{str(self.rand)})'
        notcor_load = f'@NotCorrect{str(self.rand)}'

        string_condition = f'{correct_label}, D=-1, {continue_load}, 0;JMP, {notcor_label}, D=0, {continue_load}, 0;JMP , {continue_label}'
        if command == T_ADD:
            self._Stack2D()
            self._writeCode('@add, M=D') # RAM[SP] = D
            self._Stack2D()
            self._writeCode('@add, D=M, @SP, A=M, D=M+D')
            self._D2Stack()
        elif command == T_SUB:
            self._Stack2D()
            self._writeCode('@sub, M=D') # RAM[SP] = D
            self._Stack2D()
            self._writeCode('@sub, D=M, @SP, A=M, D=M-D')
            self._D2Stack()
        elif command == T_NEG:
            self._Stack2D()
            self._writeCode('@0, D=A-D')
            self._D2Stack()
        elif command == T_EQ:
            self._Stack2D()
            self._writeCode('@eq, M=D') # RAM[eq] = D
            self._Stack2D()
            self._writeCode('@eq, D=M, @SP, A=M, D=M-D')
            self._writeCode(f'{correct_load}, D;JEQ, {notcor_load}, 0;JMP')  # True = -1, False = 0
            self._writeCode(string_condition)
            self._D2Stack()
        elif command == T_GT:
            self._Stack2D()
            self._writeCode('@gt, M=D') # RAM[SP] = D
            self._Stack2D()
            self._writeCode('@gt, D=M, @SP, A=M, D=M-D')
            self._writeCode(f'{correct_load}, D;JGT, {notcor_load}, 0;JMP')  # True = -1, False = 0
            self._writeCode(string_condition)
            self._D2Stack()
        elif command == T_LT:
            self._Stack2D()
            self._writeCode('@lt, M=D') # RAM[SP] = D
            self._Stack2D()
            self._writeCode('@lt, D=M, @SP, A=M, D=M-D')
            self._writeCode(f'{correct_load}, D;JLT, {notcor_load}, 0;JMP')  # True = -1, False = 0
            self._writeCode(string_condition)
            self._D2Stack()
        elif command == T_AND:
            self._Stack2D()
            self._writeCode('@and, M=D') # RAM[SP] = D
            self._Stack2D()
            self._writeCode('@and, D=M, @SP, A=M, D=D&M')
            # self._writeCode(f'{correct_load}, D;JLT, {notcor_load}, 0;JMP')  # True = -1, False = 0
            # self._writeCode(string_condition)
            self._D2Stack()
        elif command == T_OR:
            self._Stack2D()
            self._writeCode('@or, M=D') # RAM[SP] = D
            self._Stack2D()
            self._writeCode('@or, D=M, @SP, A=M, D=D|M')
            self._D2Stack()
        elif command == T_NOT:
            self._Stack2D()
            self._writeCode('D=!D')
            self._D2Stack()
        else:
            raise(ValueError, 'Bad arithmetic command')
        
    def writePushPop(self, commandType, segment, index):
        """
        Write Hack code for 'commandType' (C_PUSH or C_POP).
        'segment' (string) is the segment name.
        'index' (int) is the offset in the segment.
        e.g., for the VM instruction "push constant 5",
        segment has the value "constant" and index has the value 5.
        TODO - Stage I - push constant only
        TODO - Stage II - See Figure 7.6 and pp. 142-3
        """
        if commandType == C_PUSH:
            self._writeComment("push %s %d" % (segment, index))
            if segment == T_CONSTANT: 
                self._writeCode(f'@{index}, D=A')
                self._D2Stack()
            elif segment == T_STATIC:
                self._writeCode(f'@{self.fileName}.{index}')
                self._writeCode('D=M')
                self._D2Stack()
            elif segment == T_POINTER:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@3, AD=D+A')
                self._writeCode('D=M')
                self._D2Stack()
            elif segment == T_TEMP:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@5, AD=D+A')
                self._writeCode('D=M')
                self._D2Stack()
            elif segment == T_THIS:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@THIS, A=M, AD=D+A')
                self._writeCode('D=M')
                self._D2Stack()
            elif segment == T_THAT:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@THAT, A=M, AD=D+A')
                self._writeCode('D=M')
                self._D2Stack()
            elif segment == T_ARGUMENT:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@ARG, A=M, AD=D+A')
                self._writeCode('D=M')
                self._D2Stack()
            elif segment == T_LOCAL:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@LCL, A=M, AD=D+A')
                self._writeCode('D=M')
                self._D2Stack()
            

        elif commandType == C_POP:
            self._writeComment("pop %s %d" % (segment, index))
            if segment == T_STATIC:
                self._Stack2D()
                self._writeCode(f'@{self.fileName}.{index}, M=D')
            elif segment == T_POINTER:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@3, AD=D+A')
                self._writeCode(f'@R13, M=D')
                self._Stack2D()
                self._writeCode(f'@R13, A=M')
                self._writeCode('M=D')
            elif segment == T_TEMP:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@5, AD=D+A')
                self._writeCode(f'@R13, M=D')
                self._Stack2D()
                self._writeCode(f'@R13, A=M')
                self._writeCode('M=D')
            elif segment == T_THIS:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@THIS, A=M, AD=D+A')
                self._writeCode(f'@R13, M=D')
                self._Stack2D()
                self._writeCode(f'@R13, A=M')
                self._writeCode('M=D')
            elif segment == T_THAT:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@THAT, A=M, AD=D+A')
                self._writeCode(f'@R13, M=D')
                self._Stack2D()
                self._writeCode(f'@R13, A=M')
                self._writeCode('M=D')
            elif segment == T_ARGUMENT:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@ARG, A=M, AD=D+A')
                self._writeCode(f'@R13, M=D')
                self._Stack2D()
                self._writeCode(f'@R13, A=M')
                self._writeCode('M=D')
            elif segment == T_LOCAL:
                self._writeCode(f'@{index}, D=A')
                self._writeCode(f'@LCL, A=M, AD=D+A')
                self._writeCode(f'@R13, M=D')
                self._Stack2D()
                self._writeCode(f'@R13, A=M')
                self._writeCode('M=D')

        else:
            raise(ValueError, 'Bad push/pop command')


# Functions below this comment are for Project 08. Ignore for Project 07.
    def writeInit(self):
        """
        Writes assembly code that effects the VM initialization,
        also called bootstrap code. This code must be placed
        at the beginning of the output file.
        See p. 165, "Bootstrap Code"
        """
        self._writeComment("Init")
        pass

    def writeLabel(self, label):
        """ 
        Writes assembly code that effects the label command.
        See section 8.2.1 and Figure 8.6.
        """
        self._writeComment("label %s" % (label))
        pass

    def writeGoto(self, label):
        """
        Writes assembly code that effects the goto command.
        See section 8.2.1 and Figure 8.6.
        """
        self._writeComment("goto %s" % (label))
        pass

    def writeIf(self,label):
        """
        Writes assembly code that effects the if-goto command.
        See section 8.2.1 and Figure 8.6.
        """
        self._writeComment("if-goto %s" % (label))
        pass

    def writeCall(self, functionName, numArgs):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        """
        self._writeComment("call %s %d" % (functionName, numArgs))
        pass

    def writeReturn(self):
        """
        Writes assembly code that effects the return command.
        See Figure 8.5.
        """
        self._writeComment("return")
        pass

    def writeFunction(self, functionName, numLocals):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        """
        self._writeComment("function %s %d" % (functionName, numLocals))
        self.functionName = functionName # For local labels
        pass
