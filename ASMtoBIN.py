#Based off of Trung Le's code
#Finished code by: Trent Mathews


def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % bits).format(s)


def label_to_subtract(labelName,labelIndex, linePos):
    inner_count = 0
    for i in range(len(labelName)):

        tmpPOS = labelIndex[i] - linePos
        if tmpPOS < 0:
            for n in range((labelIndex[i] + 1), linePos):
                if n in labelIndex:
                    inner_count += 1
                tmpPOS = tmpPOS + inner_count
            value = format(65536 + int(tmpPOS), '016b')

        else:
            for n in range(linePos,(labelIndex[i] +1) ):
                if n in labelIndex:
                    inner_count +=1
            tmpPOS = tmpPOS - inner_count
            value = format( int(tmpPOS),'016b')
    print(str(tmpPOS)+str('!!') + value)

    return value


def asm_to_bin(asm, labelName, labelIndex):

    linePos = 0
    f = open("toBin.txt", "w+")

    for line in asm:
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("%", ",")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        if (line[0:5] == "addiu"):  # ADDIU
            line = line.replace("addiu", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001001') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:4] == "xori"):  # xori rt,rs,imm
            line = line.replace("xori", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binOUT = str('001110'+ rs+rt+str(imm) +'\n')
            f.write(binOUT)
            linePos += 1

        elif(line[0:3] == "xor") : # xor $rd ,$rs, $rt
            line = line.replace("xor", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            binOUT = str("{0}{1}{2}{3}{4}").format('000000', rs, rt, rd, '00000100110' + '\n')
            f.write(binOUT)
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

        elif(line[0:3] == "and"):  # bitwise and | and $rd,$rs,$rt
            line = line.replace("and", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            binOUT = str("{0}{1}{2}{3}{4}").format('000000', rs, rt, rd, '00000100100' + "\n")
            f.write(binOUT)
            linePos += 1

        elif (line[0:4] == "mflo"):  # lo
            line = line.replace("mflo", "")
            rd = format(int(line), '05b')
            f.write(str('0000000000000000') + str(rd) + str('00000010010') + '\n')
            linePos += 1

        elif line[0:4] == "mflo": # mflo $rd
            line = line.replace("mflo", "")
            rd = format(int(line), '05b')
            binOUT = str("0000000000000000"+rd+"00000010010" + "\n")
            f.write(binOUT)
            linePos += 1

        elif (line[0:3] == "ori"):  # ori
            line = line.replace("ori", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001101') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1
        elif line[0:2] == "or": # or $rd, rs, rt
            line = line.replace("or", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) +'00000100101'+ '\n')
            linePos += 1

        elif (line[0:4] == "mfhi"):  # MFHI
            line = line.replace("mfhi", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            f.write(str('0000000000000000') + str(rd) + str('00000010000') + '\n')
            linePos += 1

        elif (line[0:5] == "multu"):  # MULTU
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
            linePos += 1

        elif (line[0:3] == "srl"):  # SRL $rd,$rt, h
            line = line.replace("srl", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            rh = format(int(line[2]), '05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(rh) + str('000010') + '\n')
            linePos += 1

        elif (line[0:3] == "sll"):  # SLL
            line = line.replace("sll", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')
            rh = format(int(line[2]), '05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(rh) + str('000000') + '\n')
            linePos += 1

        elif (line[0:3] == "lui"):  # LUI
            line = line.replace("lui", "")
            line = line.split(",")
            rt = format(int(line[1]), '05b')
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            f.write(str('00111100000') + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:2] == "lb"):  # lb
            line = line.replace("lb", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('100000') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:2] == "sb"):  # sb
            line = line.replace("sb", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('101000') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:2] == "lw"):  # lw
            line = line.replace("lw", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('100011') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:2] == "sw"):  # sw
            line = line.replace("sw", "")
            line = line.replace(")", "")
            line = line.replace("(", ",")
            line = line.split(",")
            imm = format(int(line[1]), '016b') if (int(line[1]) > 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('101011') + str(rs) + str(rt) + str(imm) + '\n')
            linePos += 1

        elif (line[0:3] == "beq"):  # beq
            line = line.replace("beq", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                f.write(str('000100') + str(rs) + str(rt) + str(format(int(line[2]), '016b')) + '\n')

            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[2]):
                        jumpDist = -1 * (linePos + 1 + i - labelIndex[i])
                        jumpDist = bindigits(jumpDist, 16)
                        f.write(str('000100') + str(rs) + str(rt) + str(jumpDist) + str(' ') + '\n')
            linePos += 1

        elif (line[0:3] == "bne"):  # bne $rs, $rt, offset /distance
            line = line.replace("bne", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')
            rt = format(int(line[1]), '05b')

            if (line[2].isdigit()):  # First,test to see if it's a label or a integer
                f.write(str('000101') + str(rs) + str(rt) + str(format(int(line[2]), '016b')) + '\n')

            else:  # branching to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[2]):
                        #print('<, index:{0}, pos + 1: {1}'.format(labelIndex[i],linePos +1 ))
                        jumpDist = -1 * (linePos + 1 + i - labelIndex[i])
                        jumpDist = bindigits(jumpDist, 16)

            out = str( ('000101') + str(rs) + str(rt) + str(jumpDist) + '\n')
            f.write(out)
            linePos += 1

        elif (line[0:4] == "sltu"):  # sltu
            line = line.replace("sltu", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[2]), '05b')
            f.write( str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011') + '\n')
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

            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        f.write(str('000010') + str(format(int(labelIndex[i]), '026b')) + '\n')
            linePos += 1

    print(linePos)