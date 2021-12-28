// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(CHECK)
    @i //INIT i = 0
    M=0

    @8192
    D=A
    @n
    M=D //n = 8k

    @KBD
    D=M // D = RAM[24576], KEYBOARD
    @BLACK
    D;JNE //CHECKING IF PRESS != 0

(WHITE)
    @i
    D=M

    @n
    D=D-M

    @CHECK
    D;JEQ

    @SCREEN  
	D=A
	@i
	A=D+M 
    M=0 //WHITE

    @i
    M=M+1

    @WHITE
    0;JMP

(BLACK)

    @i
    D=M

    @n
    D=D-M

    @CHECK
    D;JEQ

   @SCREEN  
	D=A
	@i
	A=D+M 
    M=-1 //BLACK

    @i
    M=M+1

    @BLACK
    0;JMP