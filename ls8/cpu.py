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
        f = open( f'./examples/{str( what_to_run )}.ls8' , "r")
        content = f.readlines()

        program = []

        for i in content:
            
            if i[0] == '0':
                line_stating_0 = int(i[:8])
                program.append( line_stating_0 )
            elif i[0] == '1':
                line_stating_1 = int(i[:8])
                program.append( line_stating_1 )


        # f.close()

        print( 'program' , program )

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # Arithmetic Logic Unit
    def alu(self, op, reg_a, reg_b):

        """ALU operations."""

        print( '\nALU Called' )
        print( 'reg_a:' , reg_a )
        print( 'reg_b:' , reg_b )

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def run(self):

        """Run the CPU."""

        print( '\nRunning' )

        while self.Running_The_CPU:

            # For Debugging 🕷
            # self.trace()

            index = self.pc
            command = self.ram[ index ]

            print( '\nStep:' , self.pc , '⬇︎' )

            if command == 0b00000001:
                print( 'HLT 🛑\n' )
                self.Running_The_CPU == False
                return self.Running_The_CPU

            elif command == 0b00000000:
                print( 'NOP' )
                print( '---> No operation. Do nothing for this instruction. 💤' )
                self.pc += 1

            elif command == 0b10000010:
                print( 'LDI' )
                value1 = self.ram[ self.pc + 1 ]
                self.reg.insert( 0 , value1 )
                self.reg.pop()

                value2 = self.ram[ self.pc + 2 ]
                self.reg.insert( 0 , value2 )
                self.reg.pop()
                self.pc += 3

            elif command == 0b01000111:
                print( 'PRN' )
                print( '---> Register[0] value:' , self.reg[0] )
                self.pc += 1
            
            else:
                print( command )
                self.Running_The_CPU == False
                return self.Running_The_CPU
