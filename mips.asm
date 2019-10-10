# part 1
addi $8 , $0 , 0x2000 # 8 has starting addr
addi $9, $0 , 1 # constant 1
add $10, $0, $9 #start w/ 1
addi $19,$0,255 ######ADDED THIS FOR SIMULATION###########
addi $18, $0, 8
addi $17,$0,4
addi $12,$0,0x2000




loop_sb:
sb $10, 0($8) # store byte
addi $8, $8 ,1
addi $10, $10, 1
bne $10,$19, loop_sb


sb $10, 0($8)
sb $10, 1($8)

#end of first part

#part 2

loop_lb:
lb $11,0,($8)	#load from 8 into 11
addi $15, $0, 0 # onesCheck count
addi $16, $0, 0 # shift counter

loop_and:
andi $14,$11, 1 # andi check | 14 = AND w/ 1
beq $14, 1, ones_count # if equal to 1, increase 1 count
j shift

ones_count:
addi $15,$15, 1 # if found 1 increase One Count

shift:
srl $11, $11, 1 # shift Result | 13 = shifted right
addi $16,$16, 1 # increase shift counter
bne $16, $18 , loop_and # loop through all 8 bits
bne $15, $17, load_next # checking shift counter
addi $20,$20,1 #overall (total) counter increment

load_next:
addi $8,$8, -1  # decrease addr
bne $8 , $12,loop_lb
