"""CPU functionality."""

import sys
import os
os.system( 'clear' )

PRN = 1000111
HLT = 0b00000001
MULT = 10100010
NOP = 0b00000000
LDI = 10000010
PUSH = 1000101
POP = 1000110

class CPU:
    """Main CPU class."""

    def __init__(self):

        """Construct a new CPU."""

        print( '\nInit Called' )

        self.Running_The_CPU = True
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.SP = 7
        self.reg[ self.SP ] = 0xf4
        self.BT = { PRN: self.Print , HLT: self.HLT , MULT: self.MULT , NOP: self.NOP , LDI: self.LDI , PUSH: self.Push , POP: self.POP }

    def load(self):

        """Load a program into memory."""
        print( 'Load Called' )

        address = 0

        print( '\ncall' , '\ninterrupts' , '\nkeyboard' , '\nmult' , '\nprint8' , '\nprintstr' , '\nsctest' , '\nstack' , '\nstackoverflow' )
        what_to_run = input( '\nWhat Do You Want To Run?\n' )
        os.system( 'clear' )

        with open( f'./examples/{str( what_to_run )}.ls8' ) as f:
            for line in f:

                line = line.split("#")[0]
                line = line.strip()  # lose whitespace

                if line == '':
                    continue

                val = int(line)
                self.ram[address] = val
                address += 1

        f.close()

    # Arithmetic Logic Unit
    def alu(self, op, reg_a, reg_b):

        """ALU operations."""

        print( '\nALU Called' )
        print( 'reg_a:' , reg_a )
        print( 'reg_b:' , reg_b )

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[ reg_a ] *= self.reg[ reg_b ]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):

        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print( '\nTrace Called' )

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # ram_read() should accept the address to read and return the value stored there.
    def ram_read( self , address ):
        # print( 'Ram_Read called' )
        return self.ram[ address ]

    # ram_write() should accept a value to write, and the address to write it to.
    def ram_write( self , value , address ):
        # print( 'raw_write called' )
        self.ram[ address ] = value

    def binaryToDecimal( self , binary ): 
      
        binary1 = binary 
        decimal, i, n = 0, 0, 0
        while(binary != 0): 
            dec = binary % 10
            decimal = decimal + dec * pow(2, i) 
            binary = binary//10
            i += 1
        return decimal

    def run(self):

        """Run the CPU."""

        print( '\nRunning' )

        print( self.ram  , '\n' )

        while self.Running_The_CPU:

            # For Debugging 🕷
            # self.trace()

            # print( '\n' )

            command = self.ram[ self.pc ]

            op_a = self.ram[ self.pc + 1 ]
            op_b = self.ram[ self.pc + 2 ]

            if command in self.BT:
                
                self.BT[ command ]( op_a , op_b )

            else:

                print( f'{command} not set up yet' )
                self.Running_The_CPU == False
                return self.Running_The_CPU

    def POP( self , op_a , op_b = None ):

        # print( 'POP' )
        val = self.ram[ self.reg[ self.SP ] ]
        reg_num = self.binaryToDecimal( self.ram[ self.pc + 1 ] )
        self.reg[ reg_num ] = val  # copy val from memory at SP into register
        self.reg[ self.SP ] += 1  # increment SP

        self.pc += 2

    def Push( self , op_a , op_b ):

        # print( 'PUSH' )
        # push value from register to stack, update stack pointer

        self.reg[ self.SP ] -= 1  # decrement sp
        reg_num = self.ram[ self.pc + 1]
        reg_val = self.reg[ reg_num ]
        self.ram[ self.reg[ self.SP ] ] = reg_val  # copy reg value into memory at address SP

        self.pc += 2

    def LDI( self , op_a , op_b ):

        # print( 'LDI' )
        value = self.binaryToDecimal( op_b )

        # Put Value In Register
        self.reg[ op_a ] = value
        # print( f'Register {op_a} : {value}' )

        self.pc += 3

    def NOP( self , op_a , op_b ):
        # print( 'do nothing ( NOP )' )
        self.pc += 1

    def MULT( self , op_a , op_b ):
        # print( 'MULT' )
        self.alu( 'MUL' , op_a , op_b )
        self.pc += 3

    def HLT( self , op_a , op_b ):
        # print( '\nHLT 🛑\n' )
        self.Running_The_CPU == False
        carry_on = input( '\nDo you want to do another operation? ( y / n )\n\n' )

        if carry_on.lower() == 'y':
            os.system( 'clear' )
            cpu = CPU()
            cpu.load()
            cpu.run()
        elif carry_on.lower() == 'n':
            os.system( 'clear' )
            print( 'Thank you for using the LS8!' )
            exit()
        else:
            print( 'Invalid Response' )
            self.HLT( op_a , op_b )


    def Print( self , op_a , op_b ):

        # print( 'PRN' )
        new_val = self.binaryToDecimal( op_a )
        print( f'{self.reg[ new_val ]} - ( Print Function )' )
        self.pc += 2

