

# think about register class.... that would



# Lets use a class to define what an instruction is
# its an opcode , it has an rs, rd ,rt, imm
class Instruction():
    def __init__(self, hex_num): # everything in here is an instance variable, we are gonna read different lines of code
        # so every line should be interpreted on its own.

        hex_to_int = int(hex_num,16) # convert string to int
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
def add(instr):
    #instr.printBinary()
    print(instr.binary_S + '\n' )
    print( instr.name + " $" + str(instr.rd) +", $" + str(instr.rs) + ", $" + str(instr.rt)  + '\n')

def OR(instr):
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rd) + ", $" + str(instr.rs) + ", $" + str(instr.rt) + '\n')

# i - types
def addi (instr):
    print( instr.binary_S + '\n')
    print( instr.name + " $" + str(instr.rt) +", $" + str(instr.rs) + ", " + str(instr.imm)  + '\n')

def ori(instr):
    print(instr.binary_S + '\n')
    print(instr.name + " $" + str(instr.rt) + ", $" + str(instr.rs) + ", " + str(instr.imm) + '\n')



#python directory, like array, but uses "key" to instead of indices.
# first couple lines ... add more
#               key,    [0],  [1]
func_dict = {
            # r - types:
             '100000' : (add,'add'),
             '100101' : (OR,'or'),
             #i-types:
             '001000' : (addi, 'addi'),
             '001101': (ori,'ori')}


#first things first is read an asm file, decifer its contents to binary (homework 4),
# with the binary we can convert into machine code, and use that information to perform simulation..

# other thoughts:
#

def main():

 while(True):
     x = input("input: ( 'q' to exit)>")

     if (x == 'q'):
         print("exiting")
         break
     else:

         try: # try to create the instruction
            tmp = Instruction( x )
            function = func_dict[tmp.func][0]
            function(tmp)
         except: # if cannnot, then print supported
            print('not supported')


print(test)

if __name__ == "__main__":
    main()