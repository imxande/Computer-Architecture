"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Step 1 from Read ME
        self.RAM = [0] * 256
        self.REG = [0] * 8
        self.PC = self.REG[0]
    
    # step 2 from Read ME 
    def ram_read(self, address):
        return self.RAM[address]

    def ram_write(self, value, address):
        self.RAM[address] = value 

    # Step 4 from Read ME 
    def HLT(self, operand_a, operand_b):
        return (0, False)

    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return (3, True)

    def PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return (2, True)

    def MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        return (3, True)


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.REG[reg_a] += self.REG[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.REG[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # pass

        # Step 3 from Read ME
        halted = False

        while not halted:
            # _Instruction Register_
            IR = self.RAM[self.PC]

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if IR == LDI:
                self.REG[operand_a] = operand_b
                self.PC += 3
            elif IR == PRN:
                print(self.REG[operand_a])
                self.PC += 2
            elif IR == MUL:
                self.alu(IR, operand_a, operand_b)
                self.PC += 3
                
            # Part of Step 4 from Read ME 
            elif IR == HLT:
                sys.exit(0)
            else:
                print(f"ERROR, not working")
                sys.exit(1) 