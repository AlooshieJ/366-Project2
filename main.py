
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
    def __init__(self, address, b0, b1, b2, b3):
        self.addr= address
        self.b0 = hex(b0) # addr + 1
        self.b1 = hex(b1) #addr + 2
        self.b2 = hex(b2) #addr + 3
        self.b3 = hex(b3) #addr + 4

    def printMem(self):
        print(self.addr,self.b0,self.b1,self.b2,self.b3)
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


def mult(instr):
    # mult rs, rt
    print(instr.binary_S + '\n')
    print('mult not done')
    

# i - types
def addi(instr):
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) + '\n')
     #a = regfile.read(instr.rs) 
     #regfile.write(instr.rt, a + imm)

def ori(instr):
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) + '\n')
    # return instr.rt  or str.rs
    #a = regfile.read(instr.rs) 
    #regfile.write(instr.rt, a | imm)

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

    """
    # mem = [[0x2000,0],[0x2001,0],[0x2002,0]]
    #^^idea 1 ^^
    # VV  idea 2 VV
    #mem = [ of addr ]
    # use class to send that index of addr and set information

    MemStart = 8192 #'0x2000'
    mem_Value = [] #mem(MemStart,0,0,0,0)
 
    for i in range( 50): #this could work for each instruction instr_list:

        addr = str(hex(MemStart))
        mem_Value.append(mem(addr,0,0,0,0))

        MemStart += 4   # increment addr by 4, each will have access to every bit.

    c1= 0
    for row in mem_Value:
        if c1 % 8 == 0 :
            print('\n', end = '')

        mem_Value[c1].printMem()
        c1+=1

    # so far this is how we can change the memory values, we can probably
    # make this a function
    #mem_Value[1].addr = '000'
    #mem_Value[1].b0 = 10
    #mem_Value[1].b1 = 20
    #print(mem_Value[1].addr ,mem_Value[1].b0,mem_Value[1].b1,mem_Value[1].b2, mem_Value[1].b3 ,end = " ")
    


    tmp1 = input("input???")
    while tmp1 != 'q':
        tmp1 = input("type someting") # hex number

        try:
            x = Instruction(tmp1) # instance of the class with hex number
            instructionFunc = func_dict[x.opcode][0]
            instructionFunc(x)
        except:
            print("not supported")
        """


   # print(memaddr)

    #temp = mem(memIndex, )


    #print (temp)





if __name__ == "__main__":
    main()
