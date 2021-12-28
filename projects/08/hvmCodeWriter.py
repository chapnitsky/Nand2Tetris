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
        self.labelNumber += 1
        return "label" + str(self.labelNumber)
    
    def staticLabel(self, index):
        """Returns the static label of the index."""
        return self.functionName + '.' + str(index)

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

    def writeArithmetic(self, command):
        """
        Writes Hack assembly code for the given command.
        TODO - Stage I - see Figure 7.5 v
        """
        self._writeComment(command)
        # Arithmetic
        if command == T_ADD:
            self.binaryOp('D+A')
        elif command == T_SUB:
            self.binaryOp('A-D')
        elif command == T_NEG:
            self.unaryOp('-D')
        # Logical
        elif command == T_EQ:
            self.logicalOp('JEQ')
        elif command == T_GT:
            self.logicalOp('JGT')
        elif command == T_LT:
            self.logicalOp('JLT')
        # Bitwise
        elif command == T_AND:
            self.binaryOp('D&A')
        elif command == T_OR:
            self.binaryOp('D|A')
        elif command == T_NOT:
            self.unaryOp('!D')
        else:
            raise(ValueError, 'Bad arithmetic command')

    def binaryOp(self, comp):
        """Pops two arguments off the stack, perform comp.
        Properly manages stack pointer."""
        self.decreaseStackPointer()
        self.stackToDest('D')
        self.decreaseStackPointer()
        self.stackToDest('A')
        self.cCommand('D', comp)
        self.compToStack('D')
        self.increaseStackPointer()
    
    def unaryOp(self, comp):
        """Pop one argument off the stack, perform comp.
        Properly manages stack pointer."""
        self.decreaseStackPointer()
        self.stackToDest('D')
        self.cCommand('D', comp)
        self.compToStack('D')
        self.increaseStackPointer()
    
    def logicalOp(self, jump):
        """Pops two arguments off the stack, perform comp.
        Properly manages stack pointer.
        Returns -1 for true, 0 for false."""
        # Create new label for branching
        # Note, this does not write it to asm
        trueLabel = self._uniqueLabel()

        self.decreaseStackPointer()
        self.stackToDest('D')
        self.decreaseStackPointer()
        self.stackToDest('A')
        self.cCommand('D', 'A-D')
        self.compToStack('-1')
        self.aCommand(trueLabel)
        self.cCommand(None, 'D', jump)
        self.compToStack('0')
        self.lCommand(trueLabel)
        self.increaseStackPointer()

    
     # Register manipulators
    def registerAddress(self, segment, index):
        """Read the address of the register (segment index) into A and D."""
        segments = {'pointer': 3, 'temp': 5, 'local': 'LCL', 'argument': 'ARG',
                'this': 'THIS', 'that': 'THAT', 'static': self.staticLabel(index) }

        self.aCommand(index)
        self.cCommand('D', 'A')
        self.aCommand(segments[segment])
        if (segment in ['local', 'argument', 'this', 'that']):
            self.cCommand('A', 'M')
        self.cCommand('AD', 'D+A')


    # Write to stack commands
    def constToStack(self, const):
        """Place value at address to stack."""
        self.aCommand(const)
        self.cCommand('D', 'A')
        self.compToStack('D')

    def compToStack(self, comp):
        """Place the computation into the top of stack."""
        self.loadSP()
        self.cCommand('M', comp)

    def regToStack(self, segment, index):
        """Place the value of the register on the stack."""
        self.registerAddress(segment, index)
        self.cCommand('D', 'M') # compToStack overwrites A, so move to D first
        self.compToStack('D')


    # Read from stack commands
    def stackToDest(self, dest):
        """Place the value in the stack in the dest."""
        self.loadSP()
        self.cCommand(dest, 'M')

    def stackToReg(self, segment, index):
        """Place the value in the stack into the appropriate register."""
        self.registerAddress(segment, index)
        self.aCommand('R13')
        self.cCommand('M', 'D')
        self.stackToDest('D')
        self.aCommand('R13')
        self.cCommand('A', 'M')
        self.cCommand('M', 'D')


    # Stack pointer manipulators
    def increaseStackPointer(self):
        """Increase the stack pointer."""
        self.aCommand('SP')
        self.cCommand('M', 'M+1')

    def decreaseStackPointer(self):
        """Decrease the stack pointer."""
        self.aCommand('SP')
        self.cCommand('M', 'M-1')

    def loadSP(self):
        self.aCommand('SP')
        self.cCommand('A', 'M')


    # Command Writers
    def cCommand(self, dest, comp, jump = None):
        """Write out a C command in Hack assembly."""
        if (dest != None):
            self.write(dest + '=')
        self.write(comp)
        if (jump != None):
            self.write(';' + jump)
        self.write('\n')

    def aCommand(self, addr):
        """Write out an A command in Hack assemply."""
        self.write('@' + str(addr) + '\n')

    def lCommand(self, label):
        """Creates a new (label) for the assembler."""
        self.write('('+label+')\n')

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
                self.constToStack(index) 
            elif segment == T_STATIC:
                temp = '@' + self.fileName.split(".")[0] + '.' + str(index) + ', D=M, '
                temp += '@SP, A=M, M=D, @SP, M=M+1'
                self._writeCode(temp)
                return
            else: # argument, local, this, that
                self.regToStack(segment, index)
            self.increaseStackPointer()

        elif commandType == C_POP:
            self._writeComment("pop %s %d" % (segment, index))

            if segment == T_STATIC:
                temp = '@SP, M=M-1, A=M, D=M, '
                temp += '@' + self.fileName.split(".")[0] + '.' + str(index) + ', M=D, '
                self._writeCode(temp)
                return
                
            self.decreaseStackPointer()
            self.stackToReg(segment, index)
            
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
        self.aCommand('256')
        self.cCommand('D', 'A')
        self.aCommand('SP')
        self.cCommand('M', 'D')
        self.writeCall('Sys.init', 0)

    def writeLabel(self, label):
        """ 
        Writes assembly code that effects the label command.
        See section 8.2.1 and Figure 8.6.
        """
        self._writeComment("label %s" % (label))
        self.lCommand(label)

    def writeGoto(self, label):
        """
        Writes assembly code that effects the goto command.
        See section 8.2.1 and Figure 8.6.
        """
        self._writeComment("goto %s" % (label))
        self.aCommand(label)
        self.cCommand(dest=None, comp='0', jump='JMP') # Unconditional jump

    def writeIf(self,label):
        """
        Writes assembly code that effects the if-goto command.
        See section 8.2.1 and Figure 8.6.
        """
        self._writeComment("if-goto %s" % (label))
        self.decreaseStackPointer()
        self.stackToDest('D') # Pop top value off stack
        self.aCommand(label) # Load jump point
        self.cCommand(dest=None, comp='D', jump='JNE') # Jump if != 0

    def writeCall(self, functionName, numArgs):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        """
        return_address = self._uniqueLabel()
        self._writeComment("call %s %d" % (functionName, numArgs))
        self.constToStack(return_address)
        self.increaseStackPointer()

        self.aCommand('LCL')	
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        self.aCommand('ARG')
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        self.aCommand('THIS')
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        self.aCommand('THAT')
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        # ARG = SP - numArgs - 5
        self.aCommand('SP')         # A=SP
        self.cCommand('D', 'M')     # D=M=SP
        self.aCommand(numArgs)      # A=numArgs
        self.cCommand('D', 'D-A')   # D=D-A=SP-numArgs
        self.aCommand('5')          # A=5
        self.cCommand('D', 'D-A')   # D=D-A=SP-numArgs-5

        self.aCommand('ARG')
        self.cCommand('M', 'D')

        # LCL = SP
        self.aCommand('SP')
        self.cCommand('D', 'M')
        self.aCommand('LCL')
        self.cCommand('M', 'D')

        # goto functionName
        self.aCommand(functionName)
        self.cCommand(None, '0', 'JMP')

        self.lCommand(return_address)

    def writeReturn(self):
        """
        Writes assembly code that effects the return command.
        See Figure 8.5.
        """
        self._writeComment("return")
        # FRAME = LCL
        self.aCommand('LCL')
        self.cCommand('D', 'M')
        self.aCommand('R15')            # R15 = FRAME = LCL
        self.cCommand('M', 'D')

        # RET = *(FRAME - 5)
        # D is still FRAME
        self.aCommand('5')                  # A=5
        self.cCommand('A', 'D-A')           # A=FRAME-5
        self.cCommand('D', 'M')             # D=M=*(FRAME-5)
        self.aCommand('R14')                # R14 = RET
        self.cCommand('M', 'D')             # RET = *(FRAME-5)

        # *ARG=pop()
        self.decreaseStackPointer()
        self.registerAddress('argument', '0') # AD = ARG
        self.aCommand('R13')
        self.cCommand('M', 'D')             # *R13=ARG
        self.stackToDest('D')               # D=*SP
        self.aCommand('R13')
        self.cCommand('A', 'M')             # A=*R13=ARG
        self.cCommand('M', 'D')             # *(ARG)=*SP

        # SP = ARG + 1
        self.aCommand('ARG')
        self.cCommand('D', 'M')             # D=ARG
        self.aCommand('SP')
        self.cCommand('M', 'D+1')           # SP = ARG+1

        self.aCommand('R15')
        self.cCommand('D', 'M')
        self.cCommand('D', 'D-1')
        self.aCommand('R15')
        self.cCommand('M', 'D')
        self.cCommand('A', 'D')
        self.cCommand('D', 'M')
        self.aCommand('THAT')
        self.cCommand('M', 'D')             # THAT=*(FRAME-1)

        self.aCommand('R15')
        self.cCommand('D', 'M')
        self.cCommand('D', 'D-1')
        self.aCommand('R15')
        self.cCommand('M', 'D')
        self.cCommand('A', 'D')
        self.cCommand('D', 'M')
        self.aCommand('THIS')
        self.cCommand('M', 'D')             # THIS=*(FRAME-2)

        self.aCommand('R15')
        self.cCommand('D', 'M')
        self.cCommand('D', 'D-1')
        self.aCommand('R15')
        self.cCommand('M', 'D')
        self.cCommand('A', 'D')
        self.cCommand('D', 'M')
        self.aCommand('ARG')
        self.cCommand('M', 'D')             # ARG=*(FRAME-3)

        self.aCommand('R15')
        self.cCommand('D', 'M')
        self.cCommand('D', 'D-1')
        self.aCommand('R15')
        self.cCommand('M', 'D')
        self.cCommand('A', 'D')
        self.cCommand('D', 'M')
        self.aCommand('LCL')
        self.cCommand('M', 'D')             # LCL=*(FRAME-4)

        # Load the value of return address
        self.aCommand('R14')                # A=R14=RET
        self.cCommand('A', 'M')             # A=*RET

        # goto RET
        self.cCommand(None, '0', 'JMP')

    def writeFunction(self, functionName, numLocals):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        """
        self._writeComment("function %s %d" % (functionName, numLocals))
        self.functionName = functionName # For local labels
        self.writeLabel(functionName)
        for i in range(int(numLocals)):
            self.constToStack(0)
            self.increaseStackPointer()
