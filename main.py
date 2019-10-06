# lui, ori, addi, multu, mfhi, mflo, xor, sll, srl, sb, sw, lb, sltu, beq, bne, and
# think about register class.... that would
from ASMtoBIN import *
import time
# lets create a list of indexes we dont want for the registers
# ex:
# pc  = [34],
# lo = [32], hi ...= data[33]
#[1] -[30] available
#[0] = 0 always if they index 0 , it returns 0 :))))) so wise
class registerfile():
    def __init__(self):
        self.data = []
        for i in range(35):
            self.data.append(0x00000000)
    def read(self, readindex): 
        if(readindex == 0): 
            return 0
        return self.data[readindex]

    def write(self, writeindex, writeback_value):
        if(writeindex != 0):
            self.data[writeindex] = writeback_value

    def writeHi(self, writeback_value):
        self.data[33] = writeback_value

    def writeLo(self, writebackvalue):
        self.data[32] = writeback_value

    def movefromHi(self, destindex):
        self.data[destindex] = self.data[33]

    def movefromLo(self, destindex):
        self.data[destindex] = self.data[32]

    def readpc(self):
        return self.data[34]

    def read_and_updatepc(self):
        temp = self.data[34]
        self.data[34] += 4
        return temp
    def printRegs(self):
        print("Reg:{0} = 0x{1}".format('pc', format(self.readpc()),'08x' ) )

        for i in range(32):
            if i == 0:
                pass
            hex_tmp = format(self.read(i),'08x')
            print("Reg:{0} = 0x{1}".format(i,hex_tmp) )
            time.sleep(.25)

        print("Reg:{0} = 0x{1}".format('lo', format(self.read(32)),'08x' ) )
        print("Reg:{0} = 0x{1}".format('hi', format(self.read(33)),'08x' ) )



regfile = registerfile()
class mem():
    def __init__(self, address, b0, b1, b2, b3): # this might be backwards... idk

        self.addr = address
        self.b0 = b0 # addr + 1
        self.b1 = b1 # addr + 2
        self.b2 = b2 # addr + 3
        self.b3 = b3 # addr + 4
        self.data = str(self.b3) + str(self.b2) + str(self.b1) + str(self.b0)

    #def write(self, addr):
    #    self.data.append(self.b3+self.b2+self.b1+self.b0)
    def printMem(self ):
        print(self.data + str('|'), end=" ")
       # print(str(self.addr) + str("  ") + self.data, end=" ")

# note, doesnt not work with negatives
    def writeMem(self, address, value):

        tmp = str( format(int(value),'016b'))
        # 0|0|0|0|0|0|0|0
        # 0,1,2,3,4,5,6,7
        #-8,7,6,5,4,3,2,1
        #print(tmp)
        #print(tmp[-2:], tmp[-4:-2], tmp[-6:-4],tmp[-8:-6] )
        self.b0 = tmp[-2:]
        self.b1 = tmp[-4:-2]
        self.b2 = tmp[-6:-4]
        self.b3 = tmp[-8:-6]
        self.data = str(self.b3) + str(self.b2) + str(self.b1) + str(self.b0)

    #def loadMem(self,addr):
        #return self.data

def find_memory_address(address): # dont need this, we have a way of incrementing pc


    if address[0:7] == '0x3000':
        # not done might not need
        return 8192 + 4(1)

    elif address[0:2] == '0x2':
        to_int = (int(address[2:],16))
        return to_int/20

    else:
        print('not supported')



        # print(self.addr,self.b0 + self.b1 + self.b2 + self.b3, end=" ")
# Lets use a class to define what an instruction is
# its an opcode , it has an rs, rd ,rt, imm
# note: add instruction type detection, so we can split up the dictionary...
class Instruction():
    def __init__(self, hex_num): # everything in here is an instance variable, we are gonna read different lines of code
        # so every line should be interpreted on its own.

        hex_to_int = int(hex_num ,16) # convert string to int
        self.hexCode= hex(hex_to_int)

        # create a binary string
        self.binary_S = format(hex_to_int, '032b') # create a string of binary coding

        self.opcode = self.binary_S[0:6] # check first 6 bits to determine type.


        if self.opcode == '000000':  # all r_types have this opcode, and function is the last 6 bits
            self.func = self.binary_S[26:32]
            self.type = 'r_type'
            self.name = r_type[self.func][1]
        elif(self.opcode == '000010'):  # check for j_ type
            self.func = self.opcode
            self.type = 'j_type'
            self.name = j_type[self.opcode][1]

            if self.binary_S[6] == '1':  # check the immediate for negative numbers and convert if needed
                self.imm = -((int(self.binary_S[6:], 2) ^ 0xFFFF) + 1)

            else:
                self.imm = int(self.binary_S[6:], 2)

        else: # i type
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
        self.h =  int(self.binary_S[21:26], 2)



    def printBinary(self):
        print(self.binary_S)





# functions( instruc) these should do the actual instructions
# currently just outputting to check if they work.
# r- types
def add (instr):
    # addi rd,rs,rt
    #print(instr.binary_S)
    print( instr.name + " $" + str(instr.rd) +", $" + str(instr.rs) + ", $" + str(instr.rt))
    a = regfile.read(instr.rs)
    b = regfile.read(instr.rt)
    regfile.write(instr.rd, a + b)

def OR(instr):
    # or rd, rs, rt
    #print(instr.binary_S)
    print(instr.name + " $" + str(instr.rd) + ", $" + str(instr.rs) + ", $" + str(instr.rt))
    a = regfile.read(instr.rs)
    b = regfile.read(instr.rt)
    regfile.write(instr.rd, a | b)


def mult(instr):
    # mult rs, rt
    #print(instr.binary_S)
    print(instr.name + " $" + str(instr.rs) + ", $" + str(instr.rt))
    
def slt(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = regfile.read(instr.rs)
    b = regfile.read(instr.rt)
    if(a < b):
        regfile.write(instr.rd, 1)
    else:
        regfile.write(instr.rd, 0)
    
def xor(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = regfile.read(instr.rs) 
    b = regfile.read(instr.rt)
    regfile.write(instr.rd, a ^ b)


def multu(instr):
    print("{0} ${1}, ${2}".format(instr.name, instr.rs, instr.rt))
    #a = regfile.read(instr.rs)
    #b = regfile.read(instr.rt)
    #c, d = divmod((a * b), (2^^32))
    #regfile.writeHi(c)
    #regfile.writeLo(d)
   
def AND(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))
    a = regfile.read(instr.rs)
    b = regfile.read(instr.rt)
    regfile.write(instr.rd, a & b)

def mfhi(instr):
    print("{0} ${1}".format(instr.name, instr.rd))
    regfile.movefromHi(instr.rd)

def mflo (instr):
    print("{0} ${1}".format(instr.name, instr.rd))
    regfile.movefromLo(instr.rd)

def sll(instr):
    print("{0} ${1}, ${2}, {3}".format(instr.name, instr.rd, instr.rt, instr.h))

def srl(instr):
    print("{0} ${1}, ${2}, {3}".format(instr.name, instr.rd, instr.rt, instr.h))

def sltu(instr):
    print("{0} ${1}, ${2}, ${3}".format(instr.name, instr.rd, instr.rs, instr.rt))


# i - types
def addi(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) )
    a = regfile.read(instr.rs)
    regfile.write(instr.rt, a + instr.imm)

def addiu(instr):
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) )

def ori(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) )
    #return instr.rt  or str.rs
    a = regfile.read(instr.rs) 
    regfile.write(instr.rt, a | instr.imm)

def xori(instr):
    print("{0} ${1}, ${2}, {3}\n".format(instr.name, instr.rt, instr.rs, instr.imm))
    a = regfile.read(instr.rs)
    regfile.write(instr.rt, a ^ instr.imm)

def lui(instr):
    print("{0} ${1}, {2}").format(instr.name,instr.rt,instr.imm)

def lw(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", " + str(instr.imm) + "($" + str(instr.rs) + ')')

def sw(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", " + str(instr.imm) + "($" + str(instr.rs) + ')')

def lb(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", " + str(instr.imm) + "($" + str(instr.rs) + ')')

def sb(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", " + str(instr.imm) + "($" + str(instr.rs) + ')')

def beq(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rs) + ", $" + str(instr.rt) + ", " + str(instr.imm))

def bne(instr):
    #print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rs) + ", $" + str(instr.rt) + ", " + str(instr.imm))

# jump
def j (instr):
    print(instr.name + str(" ") + str(instr.imm))
    regfile.write(34,regfile.readpc())




# python directory, like array, but uses "key" to instead of indices.
# first couple lines ... add more
# function table in a way..
#               key,    [0],  [1]
r_type = {
    # r - types:
    '100000': (add, 'add'),
    '100101': (OR, 'or'),
    '011000': (mult, 'mult'),
    '011001': (multu,'multu'),
    '010000': (mfhi,'mfhi'),
    '010010':(mflo,'mflo'),
    '100110':(xor,'xor'),
    '000000': (sll,'sll'),
    '000010': (srl,'srl'),
    '101011':(sltu,'sltu'),
    '100100':(AND,'and'),
    '101010':(slt,'slt')
}
i_type = {
    # i-types:
    '001000': (addi, 'addi'),
    '001101': (ori, 'ori'),
    '100011': (lw, 'lw'),
    '001110': (xori,'xori'),
    '001111': (lui,'lui'),
    '101000': (sb,'sb'),
    '101011': (sw,'sw'),
    '100000': (lb,'lb'),
    '000100': (beq,'beq'),
    '000101': (bne,'bne'),
    '001001': (addiu,'addiu')
}
j_type = {
    '000010': (j, 'j')

}

# define registers as dictionary
hex_nums = { '0x0': 0,
             '0x1': 1,
             '0x2': 2,
             '0x3': 3,
             '0x4': 4,
             '0x5': 5,
             '0x6': 6,
             '0x7': 7,
             '0x8': 8,
             '0x9': 9,
             '0xa': 10,
             '0xb': 11,
             '0xc': 12,
             '0xd': 13,
             '0xe': 14,
             '0xf': 15,
             'PC': 0
}


# first things first is read an asm file, decipher its contents to binary (homework 4),
# with the binary we can convert into machine code, and use that information to perform simulation..
# asm = machine code
def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0


    for line in asm:
        line = line.replace(" ", "")
        if line.find(":") != -1:
            labelName.append(line[0:line.index(':')])  # save label name from each read line into array
            labelIndex.append(lineCount)  # save label's index
            asm[lineCount] = line[line.index(':') +1 :]
        lineCount += 1



# other thoughts:

def main():
    # input asm file
    h = open("mips.asm",'r')
    binF = open("toBin.txt",'r') # binary file
    asm = h.readlines()
    instr_list = [] # what we read from file
    labelName = []
    labelIndex = []
    lineCount = 0

#   saving label and their index.
    for i in range (asm.count('\n')):
        asm.remove('\n')


    saveJumpLabel(asm,labelIndex,labelName)


    print(labelName, labelIndex)
    for line in asm:
        line = line.replace('$', "")
        line = line.replace('\n','')
        line = line.replace('#','')
        line = line.replace('zero','0')

        if line.find(':') != -1 :
            pass
            # asd
        else:
            instr_list.append(line) # creates an array of every instruction in the file

    print("label 1{0} label2 {1}".format(instr_list[2], instr_list[12]) )
    # writes binary of assembly code to file
    asm_to_bin(instr_list,labelName, labelIndex)
    print("label 1{0} label2 {1}".format(instr_list[2], instr_list[12]) )

    """"
    Now we have each instruction at an index, need to convert it to binary...
    read from the new file created, create an instance of the class with every line.
    
    """
    sim_instr = []
    lineCount = 0
    for binary in binF.readlines():
        binary = binary.replace('\n','')
        to_hex = hex(int(binary,2))
        print(to_hex)
        x = Instruction(to_hex)
        sim_instr.append(x)
        sim_instr.append('')
        sim_instr.append('')
        sim_instr.append('')
        print(lineCount /4,end = ' ')
        # debuging
        if sim_instr[lineCount].type == 'r_type':
            instructionFunc = r_type[sim_instr[lineCount].func][0]

        elif sim_instr[lineCount].type == 'i_type':
            instructionFunc = i_type[sim_instr[lineCount].func][0]
        else:
            instructionFunc = j_type[sim_instr[lineCount].func][0]

        instructionFunc(sim_instr[lineCount])

        lineCount += 4

    """
     # THIS is the loop for the similator. only tested infinite loop w/ jump instruction
     # pc increments correctly
    pc = regfile.data[34]
    print("pc= {0} reg 3 = {1}".format(pc, regfile.read(3), '08x'))

    while pc < lineCount * 4:
        if pc % 4 == 0:
            if sim_instr[pc].type == 'r_type':
                instructionFunc = r_type[sim_instr[pc].func][0]

            elif sim_instr[pc].type == 'i_type':
                instructionFunc = i_type[sim_instr[pc].func][0]
            else:
                instructionFunc = j_type[sim_instr[pc].func][0]

            instructionFunc(sim_instr[pc])
            pc = regfile.read_and_updatepc()
        #regfile.printRegs()
        #print("pc= {0} reg 3 = 0x{1}".format(pc,format(regfile.read(3), '08x') ))
        time.sleep(1)
    """


    # use class to send that index of addr and set information
    MemStart = 8192 #'0x2000'
    mem_Value = [] #mem(MemStart,0,0,0,0)

    for i in range( 1025): #this could work for each instruction instr_list: -> loop 1025
        addr = str(hex(MemStart))
        mem_Value.append(mem(addr, 0, 0, 0, 0))
        MemStart += 4   # increment addr by 4, each will have access to every bit.


#take as string..
    # look at last 3 bits / 4 know index number

    # l = 0
    # print('Address | (+0)  | (+4)  | (+8) | (+c)  | (+10)  | (+14) | (+18)  | (+1c)')
    # for row in mem_Value:
    #     if int(row.addr, 16) % (4*8) == 0:
    #          print( '\n', end="")
    #          print(str(row.addr) + '|', end=" ")
    #     # new way to write to memory. kinda slow because array O(N)
    #     row.writeMem(row.addr, l + 1)
    #     l += 1
    #     row.printMem()

    # the old way to change memory.
    # mem_Value[100].printMem()
    # mem_Value[100].writeMem(100,101010)
    # mem_Value[100].printMem()


if __name__ == "__main__":
    main()
