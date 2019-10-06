
# think about register class.... that would
from ASMtoBIN import *

class registerfile():
    def __init__(self):
        self.data = []
        for i in range(34):
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
        return self.data[0]
    def read_and_updatepc(self):
        temp = self.data[0]
        self.data[0] += 4
        return temp
#regfile = registerfile()
class mem():
    def __init__(self, address, b0, b1, b2, b3): # this might be backwards... idk

        self.addr = address
        self.b0 = b0# addr + 1
        self.b1 = b1 #addr + 2
        self.b2 = b2 #addr + 3
        self.b3 = b3#addr + 4
        self.data = str(self.b3) + str(self.b2) + str(self.b1) + str(self.b0)

    #def write(self, addr):
    #    self.data.append(self.b3+self.b2+self.b1+self.b0)
    def printMem(self ):
        print(self.data + str('|'), end= " ")
       # print(str(self.addr) + str("  ") + self.data, end=" ")

# note, doesnt not work with negatives
    def writeMem(self,addres, value):

        tmp = str( format(int(value),'08b'))
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
        else:  # in this case the only else is type i
            self.func = self.opcode
            self.type = 'i_type'

        # assign what the registers should be
        self.rs = int(self.binary_S[6:11], 2)
        self.rt = int(self.binary_S[11:16], 2)
        self.rd = int(self.binary_S[16:21], 2)

        if self.binary_S[16] == '1':  # check the immediate for negative numbers and convert if needed
            self.imm = -((int(self.binary_S[16:32], 2) ^ 0xFFFF) + 1)
        else:
            self.imm = int(self.binary_S[16:32], 2)
        try:
            self.name = func_dict[self.func][1]  # this will lookup the string name of the function in func_dict
        except:
            self.name = 'null'

    def printBinary(self):
        print(self.binary_S)





# functions( instruc) these should do the actual instructions
# currently just outputting to check if they work.
# r- types
def add (instr):
    # addi rd,rs,rt
    print(instr.binary_S + '\n' )
    print( instr.name + " $" + str(instr.rd) +", $" + str(instr.rs) + ", $" + str(instr.rt) + '\n')
    #a = regfile.read(instr.rs)
    #b = regfile.read(instr.rt)
    #regfile.write(instr.rd, a + b)

def OR(instr):
    # or rd, rs, rt
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rd) + ", $" + str(instr.rs) + ", $" + str(instr.rt) + '\n')
    #a = regfile.read(instr.rs)
    #b = regfile.read(instr.rt)
    #regfile.write(instr.rd, a | b)


def mult(instr):
    # mult rs, rt
    print(instr.binary_S + '\n')
    print('mult not done')
    
#def slt(instr):
    #print("{0} ${1}, ${2}, ${3}\n".format(instr.name, instr.rd, instr.rs, instr.rt))
    #a = regfile.read(instr.rs)
    #b = regfile.read(instr.rt)
    #if(a < b):
    #   regfile.write(instr.rd, 1)
    # else:
    #   regfile.write(instr.rd, 0)
    
#def xor(instr):
    #print("{0} ${1}, ${2}, ${3}\n".format(instr.name, instr.rd, instr.rs, instr.rt))
    #a = regfile.read(instr.rs)
    #b = regfile.read(instr.rt)
    #regfile.write(instr.rd, a ^ b)

# i - types
def addi(instr):
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) + '\n')
     #a = regfile.read(instr.rs) 
     #regfile.write(instr.rt, a + instr.imm)

def ori(instr):
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) + '\n')
    # return instr.rt  or str.rs
    #a = regfile.read(instr.rs) 
    #regfile.write(instr.rt, a | instr.imm)

    
#def xori(instr):
    #print("{0} ${1}, ${2}, {3}\n".format(instr.name, instr.rt, instr.rs, instr,imm))
    #a = regfile.read(instr.rs)
    #regfile.write(instr.rt, a ^ instr.imm)

# python directory, like array, but uses "key" to instead of indices.
# first couple lines ... add more
# funciton table in a way..
#               key,    [0],  [1]
func_dict = {
    # r - types:
    '100000': (add, 'add'),
    '100101': (OR, 'or'),
    '011000': (mult, 'mult'),
    # i-types:
    '001000': (addi, 'addi'),
    '001101': (ori, 'ori')}

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


# first things first is read an asm file, decifer its contents to binary (homework 4),
# with the binary we can convert into machine code, and use that information to perform simulation..
# asm = machine code
def saveJumpLabel(asm,labelIndex,labelName,lineCount):

    for line in asm:
        line = line.replace(" ", "")
        if ( line.find(":") != -1 ):
            labelName.append(line[0:line.index(':')])  # save label name from each read line into array
            labelIndex.append(lineCount)  # save label's index
            #asm[lineCounter] = line[line.index(':') +1 :]
        lineCount += 1

    for item in range (asm.count('\n')):

        asm.remove('\n')

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
    saveJumpLabel(asm,labelIndex,labelName,lineCount)


    for i in range (asm.count('\n')):
        asm.remove('\n')

    print(labelName, labelIndex)
    for line in asm:
        line = line.replace('$', "")
        line = line.replace('\n','')
        line = line.replace('#','')
        line = line.replace('zero','0')

        # if line.find(':') != -1 :
        #     continue
        #     # asd
        # else:
        instr_list.append(line) # creates an array of every instruciton in the file


    # writes binary of asembly code to file


    asm_to_bin(instr_list,labelName, labelIndex)
    """"
    Now we have each instruction at an index, need to convert it to binary...
    read from the new file created, create an instance of the class with every line.
    
    """
    for binary in binF.readlines():
        binary = binary.replace('\n','')
        to_hex = hex(int(binary,2))
        print(to_hex)

        try:
            x = Instruction(to_hex)  # instance of the class with hex number
            #print(x.name)
            instructionFunc = func_dict[x.func][0]
            instructionFunc(x)
        except:
            print("not supported")


    # mem = [[0x2000,0],[0x2001,0],[0x2002,0]]
    #^^idea 1 ^^
    # VV  idea 2 VV
    #mem = [ of addr ]
    # use class to send that index of addr and set information

    MemStart = 8192 #'0x2000'
    mem_Value = [] #mem(MemStart,0,0,0,0)

    for i in range( 100): #this could work for each instruction instr_list: -> loop 1025

        addr = str(hex(MemStart))
        mem_Value.append(mem(addr,0,0,0,0) )
        MemStart += 4   # increment addr by 4, each will have access to every bit.


    l = 0
    print('Address | (+0)  | (+4)  | (+8) | (+c)  | (+10)  | (+14) | (+18)  | (+1c)')
    for row in mem_Value:

        if int(row.addr,16) % (4*8) == 0 :
             print( '\n', end= "")
             print(str(row.addr)+ '|',end = " ")
        # new way to write to memory. kinda slow because array O(N)
        row.writeMem(row.addr, l + 1)
        l+= 1
        row.printMem()


    # the old way to change memory.
    # mem_Value[100].printMem()
    # mem_Value[100].writeMem(100,101010)
    # mem_Value[100].printMem()



if __name__ == "__main__":
    main()
