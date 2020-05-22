"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Step 1 from Read ME
        self.RAM = [0] * 256
        self.REG = [0] * 8
        self.PC = self.REG[0]
        self.FLAG = self.REG[4]
        self.FL = 0
        self.E = 0
        self.L = 0
        self.G = 0
        self.running = True
    
    # step 2 from Read ME 
    def ram_read(self, address):
        return self.RAM[address]

    def ram_write(self, value, address):
        self.RAM[address] = value 

    # Step 7 from Read ME
    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        with open(file_name) as f:
            lines = f.readlines()
            lines = [line for line in lines if line.startswith('0') or line.startswith('1')]
            program = [int(line[:8], 2) for line in lines]

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.REG[reg_a] += self.REG[reg_b]
        #elif op == "SUB": etc

        # Step 8 from Read ME
        elif op == "MUL":
            product = self.REG[reg_a] * self.REG[reg_b]
            self.REG[reg_a] = product
                
        # Sprint Challenge here
        elif op == "CMP":
            if self.REG[reg_a] == self.REG[reg_b]:
                self.E = 1
                self.L = 0
                self.G = 0
            elif self.REG[reg_a] <= self.REG[reg_b]:
                self.E = 0
                self.L = 1
                self.G = 0
            else:
                self.E = 0
                self.L = 0
                self.G = 1
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

        # Variables
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        PUSH = 0b01000101
        POP = 0b01000110
        MUL = 0b10100010
        JMP = 0b01010100
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110

        # Step 3 from Read ME

        while self.running:
            # _Instruction Register_
            IR = self.RAM[self.PC]

            if IR== HLT:
                self.running == False
                break

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if IR == LDI:
                self.REG[operand_a] = operand_b
                self.PC += 3

            elif IR == PRN:
                print(self.REG[operand_a])
                self.PC += 2

            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.PC += 3

            elif IR == PUSH:
                self.REG[7] -= 1
                sp = self.REG[7]
                value = self.REG[operand_a]
                self.RAM[sp] = value
                self.PC += 2
                 

            elif IR == POP:
                sp = self.REG[7]
                value = self.RAM[sp]
                self.REG[operand_a] = value
                self.REG[7] += 1
                self.PC += 2 

            # Part of Sprint Challenge CMP
            elif IR == JMP:
                self.PC = self.REG[operand_a]

            elif IR == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.PC += 3
            
            elif IR == JEQ:
                if self.E == 1:
                    self.PC = self.REG[operand_a]
                else:
                    self.PC += 2
                
            elif IR == JNE:
                if self.E == 0:
                    self.PC = self.REG[operand_a]
                else:
                    self.PC += 2
                
            # Part of Step 4 from Read ME 
            elif IR == HLT:
                halted = True

            else:
                print(f"ERROR, not working")
                sys.exit(1) 