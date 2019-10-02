#Based off of Trung Le's code
#Finished code by: Trent Mathews

# Remember where each of the jump label is, and the target location
def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            asm[lineCount] = line[line.index(":") + 1:]
        lineCount += 1
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

def main():
    labelIndex = []
    labelName = []
    f = open("convertedToBinary.txt", "w+")
    h = open("mips.asm", "r")
    asm = h.readlines()
    linePos = 0
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm, labelIndex, labelName)  # Save all jump's destinations

    for line in asm:
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        if (line[0:5] == "addiu"): # ADDIU
            line = line.replace("addiu", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001001') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001000') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:3] == "add"):  # ADD
            line = line.replace("add", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n')
            linePos += 1

        elif (line[0:5] == "multu"): # MULTU
            line = line.replace("multu", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000011001') + '\n')
            linePos += 1

        elif (line[0:4] == "mult"):  # MULT
            line = line.replace("mult", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000011000') + '\n')
            linePos += linePos

        elif (line[0:3] == "srl"): # SRL
            line = line.replace("srl", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            rh = format(int(line[2]), '05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(rh) + str('000010') + '\n')
            linePos += 1

        elif (line[0:2] == "lb"): # lb
            line = line.replace("lb", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('100000') + str(rs) +str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:2] == "sb"): # sb
            line = line.replace("sb", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('101000') + str(rs) +str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:2] == "lw"): # lw
            line = line.replace("lw", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('100011') + str(rs) +str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:2] == "sw"): # sw
            line = line.replace("sw", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('101011') + str(rs) +str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:3] == "beq"):  # beq
            line = line.replace("beq", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                f.write(str('000100') + str(rs) +str(rt) + str(format(int(line[2]), '016b')) + '\n')
                linePos += 1


            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[2]):
                        jumpDist = -1 * (linePos - labelIndex[i] - 2)
                        jumpDist = bindigits(jumpDist, 16)
                        f.write(str('000100') + str(rs) + str(rt) + str(jumpDist) + str(' ') + '\n')
                        linePos += 1

        elif (line[0:3] == "bne"):  # bne
            line = line.replace("bne", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                f.write(str('000101') + str(rs) + str(rt) + str(format(int(line[2]), '016b')) + '\n')
                linePos += 1


            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[2]):
                        jumpDist = -1*(linePos - labelIndex[i] - 2)
                        jumpDist = bindigits(jumpDist, 16)
                        f.write(str('000101') + str(rs) +str(rt) + str(jumpDist) + '\n')
                        linePos += 1

        elif (line[0:4] == "sltu"):  # sltu
            line = line.replace("sltu", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011') + '\n')
            linePos += 1

        elif (line[0:3] == "slt"):  # slt
            line = line.replace("slt", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010') + '\n')
            linePos += 1

        elif (line[0:1] == "j"):  # JUMP
            line = line.replace("j", "")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if (line[0].isdigit()):  # First,test to see if it's a label or a integer
                f.write(str('000010') + str(format(int(line[0]), '026b')) + '\n')
                linePos += 1

            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        f.write(str('000010') + str(format(int(labelIndex[i]), '026b')) + '\n')
                        linePos += 1

    f.close()


if __name__ == "__main__":
    main()