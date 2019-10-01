
# think about register class.... that would



# Lets use a class to define what an instruction is
# its an opcode , it has an rs, rd ,rt, imm
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


def ori(instr):
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) + '\n')


# python directory, like array, but uses "key" to instead of indices.
# first couple lines ... add more
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
regs = { 0: 0,
         'PC': 0

}

# first things first is read an asm file, decifer its contents to binary (homework 4),
# with the binary we can convert into machine code, and use that information to perform simulation..
def saveJumpLabel(asmMC,labelIndex,labelName):
    lineCounter = 0
    for line in asmMC:
        line = line.replace(" ", "")
        if ( line.count(":") ):
            labelName.append(line[0:line.index(':')])  # save label name from each read line into array
            labelIndex.append(lineCounter)  # save label's index
            asmMC[lineCounter] = line[line.index(":") + 1:]
            lineCounter += 1

    for item in range (asmMC.count('\n')):
        asmMC.remove('\n')

# other thoughts:
#

def main():
    # input asm file
    f = open("test.txt","w+")
    h = open("mips.asm",'r')
    asm = h.readlines()
    labelIndex = []
    labelName = []
    c = 1

    for item in range(asm.count('\n')): # removes empty lines
        asm.remove('\n')

    saveJumpLabel(asm, labelIndex, labelName)

    print(str(labelIndex) )
    print(labelName)
    print("file:")

    for line in asm:
        print( str(c) +line)
        # f.write( line )
        c+=1

"""
    # loop to test if instruction class working properly.
    while True:
        x = input("input: ( 'q' to exit)>")

        if x == 'q':
            print("exiting")
            break
        else:

            try:  # try to create the instruction
                tmp = Instruction(x)
                function = func_dict[tmp.func][0]
                function(tmp)
            except:  # if can not, then print supported
                print('not supported')

"""
    # loop to test how memory output would look



if __name__ == "__main__":
    main()


    
class registerfile():
    def init(self):
        self.data = []
        for i in range(34):
            self.data.append(0x00000000)
    def read(self, readindex): 
        if(readindex == 0) 
            return 0
        return self.data[readindex]
    def write(self, writeindex, writeback_value):
        if(writeindex != 0):
            self.data[writeindex] = writeback_value
    def writeHi(self, writeback_value):
        self.data[33] = writeback_value
    def writeLo(self, writebackvalue):
        self.data[32] = writeback_value
    def movefromHi(self, dest_index):
        self.data[destindex] = self.data[33]
    def movefromLo(self, dest_index):
        self.data[destindex] = self.data[32]
    def readpc(self):
        return self.data[0]
    def read_and_updatepc(self):
        temp = self.data[0]
        self.data[0] += 4
        return temp
 
# >>>>>>> master
