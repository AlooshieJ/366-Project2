# lui, ori, addi, multu, mfhi, mflo, xor, sll, srl, sb, sw, lb, sltu, beq, bne, and
# think about register class.... that would
import time
import os


# added for - registers
def twos_comp(number):
    return 4294967296 + int(number)


def bin_digits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % bits).format(s)


def check_base(read_in):
    to_s = str(read_in)
    if to_s[0:2] == '0x':
        return 16
    else:
        return 2


def asm_to_bin(asm, label_name, label_index):
    line_pos = 0
    f = open("toBin.txt", "w+")
    jump_dist = 0

    for line in asm:
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("%", ",")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        if line[0:5] == "addiu":  # ADDIU
            line = line.replace("addiu", "")
            line = line.split(",")
            tmp = str(line[2])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')

            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001001') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:4] == "xori":  # xori rt, rs, imm
            line = line.replace("xori", "")
            line = line.split(",")
            tmp = str(line[2])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')

            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            bin_out = str('001110' + rs + rt + str(imm) + '\n')
            f.write(bin_out)
            line_pos += 1

        elif line[0:3] == "xor":  # xor $rd ,$rs, $rt
            line = line.replace("xor", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            bin_out = str("{0}{1}{2}{3}{4}").format('000000', rs, rt, rd, '00000100110' + '\n')
            f.write(bin_out)
            line_pos += 1

        elif line[0:4] == "addi":  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")

            tmp = str(line[2])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)

            else:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')

            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001000') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:3] == "add":  # ADD
            line = line.replace("add", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n')
            line_pos += 1

        elif line[0:4] == "andi":  # ANDI
            line = line.replace("andi", "")
            line = line.split(",")

            tmp = str(line[2])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
                print("x")
            else:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')

            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001100') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:3] == "and":  # bitwise and | and $rd,$rs,$rt
            line = line.replace("and", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            bin_out = str("{0}{1}{2}{3}{4}").format('000000', rs, rt, rd, '00000100100' + "\n")
            f.write(bin_out)
            line_pos += 1

        elif line[0:4] == "mflo":  # lo
            line = line.replace("mflo", "")
            rd = format(int(line), '05b')
            f.write(str('0000000000000000') + str(rd) + str('00000010010') + '\n')
            line_pos += 1

        elif line[0:4] == "mflo":  # mflo $rd
            line = line.replace("mflo", "")
            rd = format(int(line), '05b')
            bin_out = str("0000000000000000" + rd + "00000010010" + "\n")
            f.write(bin_out)
            line_pos += 1

        elif line[0:3] == "ori":  # ori
            line = line.replace("ori", "")
            line = line.split(",")
            tmp = str(line[2])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b')
            print("binary conversion: ",imm, tmp, x)
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001101') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:2] == "or":  # or $rd, rs, rt
            line = line.replace("or", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + '00000100101' + '\n')
            line_pos += 1

        elif line[0:4] == "mfhi":  # MFHI
            line = line.replace("mfhi", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            f.write(str('0000000000000000') + str(rd) + str('00000010000') + '\n')
            line_pos += 1

        elif line[0:5] == "multu":  # MULTU
            line = line.replace("multu", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000011001') + '\n')
            line_pos += 1

        elif line[0:4] == "mult":  # MULT
            line = line.replace("mult", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000011000') + '\n')
            line_pos += 1

        elif line[0:3] == "srl":  # SRL $rd,$rt, h
            line = line.replace("srl", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            rh = format(int(line[2]), '05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(rh) + str('000010') + '\n')
            line_pos += 1

        elif line[0:3] == "sll":  # SLL
            line = line.replace("sll", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            rh = format(int(line[2]), '05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(rh) + str('000000') + '\n')
            line_pos += 1

        elif line[0:3] == "lui":  # LUI
            line = line.replace("lui", "")
            line = line.split(",")
            rt = format(int(line[0]), '05b')
            tmp = str(line[1])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')

            f.write(str('00111100000') + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:2] == "lb":  # lb
            line = line.replace("lb", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            tmp = str(line[1])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')

            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('100000') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:2] == "sb":  # sb
            line = line.replace("sb", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            tmp = str(line[1])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')

            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('101000') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:2] == "lw":  # lw
            line = line.replace("lw", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            tmp = str(line[1])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')

            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('100011') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:2] == "sw":  # sw
            line = line.replace("sw", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            tmp = str(line[1])
            if check_base(tmp) == 16:
                x = int(tmp, 16)
                imm = bin_digits(x, 16)
            else:
                imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')

            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('101011') + str(rs) + str(rt) + str(imm) + '\n')
            line_pos += 1

        elif line[0:3] == "beq":  # beq
            line = line.replace("beq", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')

            if line[2].isdigit():  # First,test to see if it's a label or a integer
                f.write(str('000100') + str(rs) + str(rt) + str(format(int(line[2]), '016b')) + '\n')

            else:  # Jumping to label
                for i in range(len(label_name)):
                    if label_name[i] == line[2]:
                        jump_dist = label_index[i] - (line_pos + 1)
                        #if jump_dist < 0:
                        #    jump_dist
                        jump_dist = bin_digits(jump_dist, 16)
                        f.write(str('000100') + str(rs) + str(rt) + str(jump_dist) + str(' ') + '\n')
            line_pos += 1

        elif line[0:3] == "bne":  # bne $rs, $rt, offset /distance
            line = line.replace("bne", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')

            if line[2].isdigit():  # First,test to see if it's a label or a integer
                f.write(str('000101') + str(rs) + str(rt) + str(format(int(line[2]), '016b')) + '\n')
                jump_dist = imm

            else:  # branching to label
                for i in range(len(label_name)):
                    if label_name[i] == line[2]:
                        jump_dist = label_index[i] - (line_pos + 1)
                        #if jump_dist < 0:
                            #jump_dist = jump_dist*-1
                        jump_dist = bin_digits(jump_dist, 16)

            out = str('000101' + str(rs) + str(rt) + str(jump_dist) + str(' ') + '\n')
            f.write(out)
            line_pos += 1

        elif line[0:4] == "sltu":  # sltu
            line = line.replace("sltu", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011') + '\n')
            line_pos += 1

        elif line[0:3] == "slt":  # slt
            line = line.replace("slt", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010') + '\n')
            line_pos += 1

        elif line[0:4] == "spec":  # special instruction
            line = line.replace("spec", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            bin_out = str("{0}{1}{2}{3}{4}").format('000000', rs, rt, rd, '00000111111' + '\n')
            f.write(bin_out)
            line_pos += 1

        elif line[0:1] == "j":  # JUMP
            line = line.replace("j", "")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if line[0].isdigit():  # First,test to see if it's a label or a integer
                f.write(str('000010') + str(format(int(line[0]), '026b')) + '\n')

            else:  # Jumping to label
                for i in range(len(label_name)):
                    if label_name[i] == line[0]:
                        f.write(str('000010') + str(format(int(label_index[i]), '026b')) + '\n')
            line_pos += 1

    print(line_pos)


def sign_extend(value, bits):
    mask = 0xffffff00
    bin_digits(value, 32)
    value = mask ^ value
    print("{:08x} ? {:08x}, value: {:08x} ".format(mask, bits, value))
    #
    # sign_bit =  1 << (bits - 1)
    # return (value & (sign_bit - 1)) - (value & sign_bit)
    return value


# lets create a list of indexes we do not want for the registers
# ex:
# pc  = [34],
# lo = [32], hi ...= data[33]
# [1] -[30] available
# [0] = 0 always if they index 0 , it returns 0 :))))) so wise
class registerFile:
    def __init__(self):
        self.data = []
        for i in range(35):
            self.data.append(0x00000000)
            
    def read(self, read_index): 
        if read_index == 0:
            return 0
        return self.data[read_index]

    def write(self, write_index, write_back_value):
        if write_index != 0:
            if write_back_value < 0:
                self.data[write_index] = twos_comp(write_back_value)
            else:
                self.data[write_index] = write_back_value
    # added this for storing...

    def write_sext(self, write_index, write_back_value):  # write w/ sign-extend
        if write_index != 0:
            tmp = hex(write_back_value)[2:]

            if write_back_value > 0:
                self.data[write_back_value] = int(tmp, 16)
            else:
                print("writing:", tmp, "to REG:", write_index)
                self.data[write_index] = sign_extend(int(tmp, 16), 32)

    def write_hi(self, write_back_value):
        self.data[33] = write_back_value

    def write_lo(self, write_back_value):
        self.data[32] = write_back_value

    def move_from_hi(self, dest_index):
        self.data[dest_index] = self.data[33]

    def move_from_lo(self, dest_index):
        self.data[dest_index] = self.data[32]

    def read_pc(self):
        return self.data[34]

    def update_pc(self):
        self.data[34] += 4

    def print_regs(self):
        for i in range(35):
            if i % 5 == 0:
                print('\n', end='')
            hex_tmp = format(self.read(i), '08x')
            if i < 10:
                print("0{0} = 0x{1}".format(i, hex_tmp), end=" ")
            else:
                print("{0} = 0x{1}".format(i, hex_tmp), end=" ")
        print('\n')


memory = []  # mem(mem_start,0,0,0,0)
reg_file = registerFile()


# msb = b3 lsb = b0
class mem:
    def __init__(self, address, b3, b2, b1, b0):

        self.addr = address
        self.b0 = b0  # addr + 0
        self.b1 = b1  # addr + 1
        self.b2 = b2  # addr + 2
        self.b3 = b3  # addr + 3
        self.data = str(self.b3) + str(self.b2) + str(self.b1) + str(self.b0)

    def print_mem(self ):  # b3 = msb , b0 = lsb
        print(" ", hex(self.addr), end=":  ")
        print("{0:02x}".format(self.b3), end="")
        print("{0:02x}".format(self.b2), end="")
        print("{0:02x}".format(self.b1), end="")
        print("{0:02x}".format(self.b0), end="")

        # print(hex(self.addr) + str(" ") + b3 + b2+ b1+ b0 + str(" | ")) #, end=" ")

# note, doesnt not work with negatives
    def writeWordMem(self, value):

        tmp = str(format(int(value), '08x'))

        # 0|0|0|0|0|0|0|0
        # 0,1,2,3,4,5,6,7
        # -8,7,6,5,4,3,2,1
        # print(tmp)
        # print("infunc: ",tmp[-2:], tmp[-4:-2], tmp[-6:-4],tmp[-8:-6] )
        self.b0 = int(tmp[-2:],   16)
        self.b1 = int(tmp[-4:-2], 16)
        self.b2 = int(tmp[-6:-4], 16)
        self.b3 = int(tmp[-8:-6], 16)
        self.data = str(self.b3) + str(self.b2) + str(self.b1) + str(self.b0)

        # def loadMem(self,addr):
        # return self.data



# print(self.addr,self.b0 + self.b1 + self.b2 + self.b3, end=" ")
# Lets use a class to define what an instruction is
# its an opcode , it has an rs, rd ,rt, imm
# note: add instruction type detection, so we can split up the dictionary...
class Instruction:
    def __init__(self, hex_num):  # all in here is an instance variable, we are gonna read different lines of code
        # so every line should be interpreted on its own.

        hex_to_int = int(hex_num, 16)  # convert string to int
        self.hexCode = hex(hex_to_int)

        # create a binary string
        self.binary_S = format(hex_to_int, '032b')  # create a string of binary coding

        self.opcode = self.binary_S[0:6]  # check first 6 bits to determine type.

        if self.opcode == '000000':  # all r_types have this opcode, and function is the last 6 bits
            self.func = self.binary_S[26:32]
            self.type = 'r_type'
            self.name = r_type[self.func][1]

        elif self.opcode == '000010':  # check for j_ type
            self.func = self.opcode
            self.type = 'j_type'
            self.name = j_type[self.opcode][1]

            if self.binary_S[6] == '1':  # check the immediate for negative numbers and convert if needed
                self.imm = -((int(self.binary_S[6:], 2) ^ 0xFFFF) + 1)

            else:
                self.imm = int(self.binary_S[6:], 2)

        elif self.opcode == '111111':  # special instruction
            self.func = self.opcode
            self.type = 'r_type'
            self.name = r_type[self.opcode][1]

        elif self.opcode == '001101':  # ori
            self.func = self.opcode
            self.type = 'i_type_special'
            self.name = i_type_special[self.opcode][1]
            self.imm = int(self.binary_S[16:32], 2)

        else:  # i type
            self.func = self.opcode
            self.type = 'i_type'
            self.name = i_type[self.func][1]

            if self.binary_S[16] == '1':  # check the immediate for negative numbers and convert if needed
                self.imm = -((int(self.binary_S[16:32], 2) ^ 0xFFFF) + 1)

            else:
                self.imm = int(self.binary_S[16:32], 2)

        # assign what the registers should be
        self.rs = int(self.binary_S[6:11], 2)
        self.rt = int(self.binary_S[11:16], 2)
        self.rd = int(self.binary_S[16:21], 2)
        self.h = int(self.binary_S[21:26], 2)

    def print_binary(self):
        print(self.binary_S)


# functions(instr) these should do the actual instructions
# currently just outputting to check if they work.
# r- types
def add(instr):
    # addi rd,rs,rt
    # print(instr.binary_S)
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)
    reg_file.write(instr.rd, a + b)
    reg_file.update_pc()


def OR(instr):
    # or rd, rs, rt
    # print(instr.binary_S)
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)
    reg_file.write(instr.rd, a | b)
    reg_file.update_pc()


def mult(instr):
    # mult rs, rt
    # print(instr.binary_S)
    print("{0} ${1}, ${2}".format(instr.name, instr.rs, instr.rt))
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)

    multiply = a * b
    c = bin_digits(multiply, 64)
    d = int(c[0:32], 2)
    e = int(c[32:64], 2)
    reg_file.write_hi(d)
    reg_file.write_lo(e)
    reg_file.update_pc()


def slt(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)
    if a < b:
        reg_file.write(instr.rd, 1)
        reg_file.update_pc()
    else:
        reg_file.write(instr.rd, 0)
        reg_file.update_pc()


def xor(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = reg_file.read(instr.rs) 
    b = reg_file.read(instr.rt)
    reg_file.write(instr.rd, a ^ b)
    reg_file.update_pc()


def multu(instr):
    print("{0} ${1}, ${2}".format(instr.name, instr.rs, instr.rt))
    # a = reg_file.read(instr.rs)
    # b = reg_file.read(instr.rt)
    # c, d = divmod((a * b), (2 ^ 32))
    # reg_file.write_hi(c)
    # reg_file.write_lo(d)
    # reg_file.update_pc()
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)

    multiply = a * b
    c = bin_digits(multiply, 64)
    d = int(c[0:32], 2)
    e = int(c[32:64],2)
    reg_file.write_hi(d)
    reg_file.write_lo(e)
    reg_file.update_pc()

def AND(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)
    reg_file.write(instr.rd, a & b)
    reg_file.update_pc()


def andi(instr):
    print("{0} ${1}, ${2}, {3}".format(instr.name, instr.rt, instr.rs, instr.imm))
    a = reg_file.read(instr.rs)
    b = instr.imm
    reg_file.write(instr.rt, a & b)
    reg_file.update_pc()


def mfhi(instr):
    print("{0} ${1}".format(instr.name, instr.rd))
    reg_file.move_from_hi(instr.rd)
    reg_file.update_pc()


def mflo(instr):
    print("{0} ${1}".format(instr.name, instr.rd))
    reg_file.move_from_lo(instr.rd)
    reg_file.update_pc()


def sll(instr):
    print("{0} ${1}, ${2}, {3}".format(instr.name, instr.rd, instr.rt, instr.h))
    a = reg_file.read(instr.rt)
    b = instr.h
    mask = 2**32 - 1
    if a < 0:
        value = (twos_comp(a) << b) & mask
        reg_file.write(instr.rd, value)
        reg_file.update_pc()
    else:
        reg_file.write(instr.rd, (a << b) & mask)
        reg_file.update_pc()


def srl(instr):
    print("{0} ${1}, ${2}, {3}".format(instr.name, instr.rd, instr.rt, instr.h))
    a = reg_file.read(instr.rt)
    b = instr.h
    mask = 2 ** 32 - 1
    if a < 0:
        value = (twos_comp(a) >> b) & mask
        reg_file.write(instr.rd, value)
        reg_file.update_pc()
    else:
        reg_file.write(instr.rd, (a >> b) & mask)
        reg_file.update_pc()
        # chop off the msb when gets past


# 64 bits... adn w/ 00000ffff for lowest 32 bits shift right 32 bits
# then xor lo right shift should add zeros

def sltu(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))

    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)
    if a < b:
        reg_file.write(instr.rd, 1)
        reg_file.update_pc()
    else:
        reg_file.write(instr.rd, 0)
        reg_file.update_pc()


# i - types
def addi(instr):
    # print(instr.binary_S + '\n')
    print("{0} ${1}, ${2}, {3}".format(instr.name, instr.rt, instr.rs, instr.imm))
    a = reg_file.read(instr.rs)
    reg_file.write(instr.rt, a + instr.imm)
    reg_file.update_pc()


def addiu(instr):
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm))
    a = reg_file.read(instr.rs)
    reg_file.write(instr.rt, a + twos_comp(instr.imm))
    reg_file.update_pc()


def ori(instr):
    # print(instr.binary_S + '\n')
    print("{0} ${1}, ${2}, {3}".format(instr.name, instr.rt, instr.rs, instr.imm))
    # return instr.rt  or str.rs
    a = reg_file.read(instr.rs)
    b = twos_comp(instr.imm)
    c = a | b
    print(hex(a), int(b), hex(c))

    reg_file.write(instr.rt, a | instr.imm)
    reg_file.update_pc()


def xori(instr):
    print("{0} ${1}, ${2}, {3}\n".format(instr.name, instr.rt, instr.rs, instr.imm))
    a = reg_file.read(instr.rs)
    reg_file.write(instr.rt, a ^ instr.imm)
    reg_file.update_pc()


def lui(instr):
    print("{0} ${1}, {2}".format(instr.name, instr.rt, instr.imm))
    a = instr.imm
    shift = a << 16
    print("a", a)
    reg_file.write(instr.rt, shift)
    reg_file.update_pc()


def lw(instr):
    # print(instr.binary_S + '\n')
    print("{0} ${1}, {3}(${2})".format(instr.name, instr.rt, instr.rs, instr.imm))

    tmpRS = reg_file.read(instr.rs)
    index = abs( tmpRS + instr.imm - int('0x2000', 16) )
    address = index // 4
    offset = index % 4
    print("loadW index: ", index, "addr: ", address, "offset: ", offset)

    if index % 4 != 0:
        print("error")
        exit(0)
    else:
       b0 = hex(memory[address].b0)[2:]
       b1 = hex(memory[address].b1)[2:]
       b2 = hex(memory[address].b2)[2:]
       b3 = hex(memory[address].b3)[2:]
       if b0 == '0':
           b0 = '00'
       if b1 == '0':
            b1 = '00'
       if b2 == '0':
            b2 = '00'
       if b3 == '0':
            b3 = '00'
       tmp = b3+b2+b1+b0
       tmp = int(tmp,16)
       print(b3,b2,b1,b0,tmp )
       reg_file.write(instr.rt,tmp)



    reg_file.update_pc()


def sw(instr):
    # print(instr.binary_S + '\n')
    print("{0} ${1}, {2}(${3})".format(instr.name, instr.rt, instr.imm, instr.rs))

    value = reg_file.read(instr.rt)
    reg_rs = reg_file.read(instr.rs)

    index = abs(reg_rs + instr.imm - int('0x2000', 16))

    address = index // 4
    remainder = index % 4
    print("store index: ", index, "addr: ", address, "value: ", end="")

    value = bin_digits(value, 32)
    print(value)
    value = int(value, 2)
    print(value)

    if index % 4 != 0:
        print("error")
        exit(0)  # this will cause code to end
    else:
        memory[address].writeWordMem(value)
        reg_file.update_pc()
        # memory[address].print_mem()


def lb(instr):  # lb rt, offset(rs)
    # print(instr.binary_S + '\n')
    print("{0} ${1}, {3}(${2})".format(instr.name, instr.rt, instr.rs, instr.imm))

    tmpRS = reg_file.read(instr.rs)
    index = abs( tmpRS + instr.imm - int('0x2000', 16) )
    address = index // 4
    offset = index % 4
    print("load index: ", index, "addr: ", address, "offset: ", offset)

    if offset == 0:
        # print("addr + 0")
        value = memory[address].b0

    elif offset == 1:
        # print("addr + 1")
        value = memory[address].b1

    elif offset == 2:
        # print("addr + 2")
        value = memory[address].b2

    elif offset == 3:
        # print("addr + 3")
        value = memory[address].b3
    reg_file.update_pc()

    # print(sign_extend(value,32))
    if value < 0:
        reg_file.write_sext(instr.rt, value)
    else:
        reg_file.write(instr.rt, value)


def sb(instr):  # b0 = msb b3 = lsb
    # print(instr.binary_S + '\n')
    print("{0} ${1}, {3}(${2})".format(instr.name, instr.rt, instr.rs, instr.imm))
    tmprs = reg_file.read(instr.rs)
    index = abs(tmprs + instr.imm - int('0x2000', 16))
    print("|{} + {} - {} |".format(tmprs, instr.imm, int('0x2000', 16)))
    address = index // 4
    offset = index % 4

    value = reg_file.read(instr.rt)
    print('value to store:', value)
    value = bin_digits(value, 32)
    print(value[:2], value[2:4], value[4:6], value[6:8])
    value = int(value[-8:], 2)
    print("index: ", index, "addr: ", address, "offset: ", offset, "value:", value)

    if offset == 0:
        # print("addr + 0")
        memory[address].b0 = value

    elif offset == 1:
        # print("addr + 1")
        memory[address].b1 = value

    elif offset == 2:
        # print("addr + 2")
        memory[address].b2 = value

    elif offset == 3:
        # print("addr + 3")
        memory[address].b3 = value

    memory[address].print_mem()
    reg_file.update_pc()


def beq(instr):
    # print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rs) + ", $" + str(instr.rt) + ", " + str(instr.imm))
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)
    tmp = instr.imm * 4
    dist = tmp + reg_file.read_pc() + 4

    print('pc=', reg_file.read_pc(), "tmp", tmp, "dist:", dist)
    print('a=', a, "b=", b, "imm= ", instr.imm)

    if a == b:
        reg_file.write(34, dist)
    else:
        reg_file.update_pc()
    # pass
    #     tmp + 4
    #     reg_file.write(34, tmp)


def bne(instr):
    # print(instr.binary_S + '\n')
    print(str(instr.name) + " $" + str(instr.rs) + ", $" + str(instr.rt) + ", " + str(instr.imm))
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)
    # dist = reg_file.read_pc()
    tmp = instr.imm * 4
    dist = tmp + reg_file.read_pc() + 4

    print('pc=', reg_file.read_pc(), "tmp", tmp, "dist:", dist)
    print('a=', a, "b=", b)
    if a != b:
        reg_file.write(34, dist)
    # elif dist == 0:
    #     reg_file.update_pc()
    else:
        reg_file.update_pc()
        # pass
    #     tmp += 4
    #     reg_filereg_file.update_pc()


# jump
def j(instr):
    print(instr.name + str(" ") + str(instr.imm))
    # oldPC = reg_file.read_pc()
    # newPC = oldPC &0xf0000000 |instr.imm << 2
    # print(oldPC, newPC )
    reg_file.write(34, 4 * instr.imm)
    # exit(0)


# special instruction
def spec(instr):
    print("{0} ${1}, ${2}, ${3}\n".format(instr.name, instr.rd, instr.rs, instr.rt))
    # mult then xor
    a = reg_file.read(instr.rs)
    b = reg_file.read(instr.rt)

    for i in range(5):
        multiply = a * b
        c = bin_digits(multiply, 64)
        d = int(c[0:32], 2)
        e = int(c[32:64], 2)

        a = d ^ e

    mask = 4294967295
    shifter_left = a << 16
    shifter_left = shifter_left & mask
    shifter_left = shifter_left >> 16
    shifter_right = a >> 16
    a = shifter_left ^ shifter_right

    shifter_left = a << 24
    shifter_left = shifter_left & mask
    shifter_left = shifter_left >> 24
    shifter_right = a << 16
    shifter_right = shifter_right & mask
    shifter_right = shifter_right >> 24

    a = shifter_left ^ shifter_right

    reg_file.write(instr.rd, a)
    reg_file.update_pc()

# python directory, like array, but uses "key" to instead of indices.
# first couple lines ... add more
# function table in a way..
#               key,    [0],  [1]


r_type = {
    # r - types:
    '100000': (add, 'add'),
    '100101': (OR, 'or'),
    '011000': (mult, 'mult'),
    '011001': (multu, 'multu'),
    '010000': (mfhi, 'mfhi'),
    '010010': (mflo, 'mflo'),
    '100110': (xor, 'xor'),
    '000000': (sll, 'sll'),
    '000010': (srl, 'srl'),
    '101011': (sltu, 'sltu'),
    '100100': (AND, 'and'),
    '101010': (slt, 'slt'),
    '111111': (spec, 'spec')  # special instruction
}
i_type_special = {
    '001101': (ori, 'ori')

}
i_type = {
    # i-types:
    '001000': (addi, 'addi'),
    '001100': (andi, 'andi'),
    '001111': (lui, 'lui'),
    '100011': (lw, 'lw'),
    '001110': (xori, 'xori'),
    '101000': (sb, 'sb'),
    '101011': (sw, 'sw'),
    '100000': (lb, 'lb'),
    '000100': (beq, 'beq'),
    '000101': (bne, 'bne'),
    '001001': (addiu, 'addiu')
}
j_type = {
    '000010': (j, 'j')}


# first things first is read an asm file, decipher its contents to binary (homework 4),
# with the binary we can convert into machine code, and use that information to perform simulation..
# asm = machine code
def saveJumpLabel(asm, label_index, label_name):
    line_count = 0

    for line in asm:
        line = line.replace(" ", "")
        if line.find(":") != -1:

            label_name.append(line[0:line.index(':')])  # save label name from each read line into array
            label_index.append(line_count)  # save label's index
            del asm[line_count]
            # asm[line_count] = line[line.index(':') +1 :]
        # elif line.find("#") != -1:
        #     asm[line_count] = line[line.index('#')+1 :]

        line_count += 1
def printallmem():
    count = 0
    #print('Address |   (+0)    |   (+4)    |   (+8)   |   (+c)    |   (+10)    |   (+14)   |   (+18)    |   (+1c)  ')
    print('Memory')
    for row in memory[:100]:
        if row.addr % (4 * 8) == 0:
            print('\n', end=" ")
        count += 1
        row.print_mem()

    print(" ")

def main():
    # input asm file
    readFile = input("select file: (testcase.asm), (hash-default.asm), (hash-plus.asm)" )
    print(readFile)

    h = open(readFile, 'r')
    bin_file = open("toBin.txt", 'w+')  # binary file
    asm = h.readlines()
    instr_list = []  # what we read from file
    label_name = []
    label_index = []
    line_count = 0
    DIC = 1
    rcount = 0
    icount = 0
    jcount = 0
    spcount = 0
    mem_start = 8192  # '0x2000'

    for i in range(1025):  # this could work for each instruction instr_list: -> loop 1025
        addr = mem_start
        memory.append(mem(addr, 0, 0, 0, 0))
        mem_start += 4  # increment addr by 4, each will have access to every bit.

    # saving label and their index.
    for i in range(asm.count('\n')):
        asm.remove('\n')

    saveJumpLabel(asm, label_index, label_name)

    print(label_name, label_index)

    # working file reads
    for line in asm:
        line = line.replace('$', "")
        line = line.replace('\n', "")
        line = line.replace('zero', '0')

        if line.find(':') != -1:
            pass
        else:

            instr_list.append(line)


    # writes binary of assembly code to file
    asm_to_bin(instr_list, label_name, label_index)
    # print("label 1{0} label2 {1}".format(instr_list[2], instr_list[12]) )

    """"
    Now we have each instruction at an index, need to convert it to binary...
    read from the new file created, create an instance of the class with every line.
    
    """
    sim_instr = []
    line_count = 0
    for binary in bin_file.readlines():
        binary = binary.replace('\n', '')
        to_hex = hex(int(binary, 2))
        #print(to_hex)
        x = Instruction(to_hex)
        sim_instr.append(x)
        sim_instr.append('')
        sim_instr.append('')
        sim_instr.append('')

        line_count += 4


    # """
    # THIS is the loop for the simulator. only tested infinite loop w/ jump instruction
    # pc increments correctly
    # print("pc= {0} reg 3 = {1}".format(pc, reg_file.read(3), '08x'))
    pc = 0
    while pc <= line_count * 4:
        pc = reg_file.read_pc()

        if pc % 4 == 0:
            # if pc == line_count * 4:
            # break
            try:
                if sim_instr[pc].type == 'r_type':
                    instr_func = r_type[sim_instr[pc].func][0]
                    rcount += 1

                elif sim_instr[pc].type == 'i_type':
                    instr_func = i_type[sim_instr[pc].func][0]
                    icount += 1
                elif sim_instr[pc].type == 'i_type_special':
                    instr_func = i_type_special[sim_instr[pc].func][0]
                    spcount += 1
                else:
                    instr_func = j_type[sim_instr[pc].func][0]
                    jcount += 1

            except:
                print("end of instr")
                break

        instr_func(sim_instr[pc])
        DIC += 1


    print('\n\nREGS:')
    reg_file.print_regs()
    printallmem()
    tmp = icount + jcount + rcount
    print('   DIC', DIC)
    

if __name__ == "__main__":
    main()
