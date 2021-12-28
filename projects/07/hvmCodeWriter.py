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
        self.labelNumber += 1;
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

    def _pushD(self):
        """
        Writes Hack assembly code to push the value from the D register 
        onto the stack.
        TODO - Stage I - see Figure 7.2
        """
        pass

    def _popD(self):
        """"
        Writes Hack assembly code to pop a value from the stack 
        into the D register.
        TODO - Stage I - see Figure 7.2
        """
        pass

    def writeArithmetic(self, command):
        """
        Writes Hack assembly code for the given command.
        TODO - Stage I - see Figure 7.5
        """
        self._writeComment(command);

        if command == T_ADD:
            pass 
        elif command == T_SUB:
            pass
        elif command == T_NEG:
            pass
        elif command == T_EQ:
            pass
        elif command == T_GT:
            pass
        elif command == T_LT:
            pass
        elif command == T_AND:
            pass
        elif command == T_OR:
            pass
        elif command == T_NOT:
            pass
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
                pass 
            elif segment == T_STATIC:
                pass
            elif segment == T_POINTER:
                pass
            elif segment == T_TEMP:
                pass
            else: # argument, local, this, that
                pass

        elif commandType == C_POP:
            self._writeComment("pop %s %d" % (segment, index))

            if segment == T_STATIC:
                pass
            elif segment == T_POINTER:
                pass
            elif segment == T_TEMP:
                pass
            else: # argument, local, this, that
                pass

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
