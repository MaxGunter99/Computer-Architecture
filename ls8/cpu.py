"""CPU functionality."""

import sys
import os
os.system( 'clear' )

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
        self.reg[ self.SP] = 0xf4

        # print( 'Running:' , self.Running_The_CPU )
        # print( 'Random Access Memory:' , self.ram )
        # print( 'PC:' , self.pc )
        # print( 'Registers:' , self.reg )

    def load(self):

        """Load a program into memory."""
        print( 'Load Called' )

        address = 0

        print( '\ncall' , '\ninterrupts' , '\nkeyboard' , '\nmult' , '\nprint8' , '\nprintstr' , '\nsctest' , '\nstack' , '\nstackoverflow' )
        what_to_run = input( '\nWhat Do You Want To Run?\n' )

        program = []

        with open( f'./examples/{str( what_to_run )}.ls8' ) as f:
            for line in f:

                line = line.split("#")[0]
                line = line.strip()  # lose whitespace

                if line == '':
                    continue

                val = int(line)
                self.ram[address] = val
                address += 1


        # f.close()

        print( 'program' , program )

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
        print( 'Ram_Read called' )
        return self.ram[ address ]

    # raw_write() should accept a value to write, and the address to write it to.
    def raw_write( self , value ):
        print( 'raw_write called' )
        pass

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
            print( '\n' )

            index = self.pc
            command = self.ram[ index ]

            if command == 0b00000001:
                print( 'HLT 🛑\n' )
                self.Running_The_CPU == False
                return self.Running_The_CPU

            elif command == 0b00000000:
                print( 'NOP' )
                print( '---> No operation. 💤' )
                self.pc += 1

            elif command == 10000010:

                print( 'LDI' )
                # Register number
                this_register = self.ram[ self.pc + 1 ]

                # Value to put in that register ( also convert to decimal )
                original = self.ram[ self.pc + 2 ]
                value = self.binaryToDecimal( original )
                # Put Value In Register
                self.reg[ this_register ] = value

                self.pc += 3

            elif command == 1000111:

                print( 'PRN' )
                this_register = self.ram[ self.pc + 1 ]
                print( '---> value:' , self.reg[0] )
                self.pc += 2

            elif command == 10100010:

                print( 'MULT' )
                register_one = self.ram[ self.pc + 1 ]
                register_two = self.ram[ self.pc + 2 ]
                self.alu( 'MUL' , register_one , register_two )

                self.pc += 3
            
            else:
                print( f'{command} not set up yet' )
                self.Running_The_CPU == False
                return self.Running_The_CPU

