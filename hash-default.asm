lui $9, 0xFA19
ori $9, $9, 0xE366
addi $8, $0, 1
addi $10, $0, 0x2020
addi $11, $0, 100

loop:
multu $8, $9
mfhi $13
mflo $14
xor $15, $13, $14


multu $15, $9
mfhi $13
mflo $14
xor $15, $13, $14


multu $15, $9
mfhi $13
mflo $14
xor $15, $13, $14


multu $15, $9
mfhi $13
mflo $14
xor $15, $13, $14


multu $15, $9
mfhi $13
mflo $14
xor $15, $13, $14


sll $16, $15, 16
srl $16, $16, 16
srl $17, $15, 16
xor  $15, $16, $17


sll $16, $15, 24
srl $16, $16, 24
sll $17, $15, 16
srl $17, $17, 24
xor $15, $16, $17


sb $15, 0($10)
addi $10, $10, 1
addi $8, $8, 1
addi $11, $11, -1
bne $11, $0, loop

addi $11, $0, 100
addi $10, $0, 0x2020
addi $23, $0, 0x2000

store_data:
add $18, $19, $0
sw $10, 0($23)
sb $18, 4($23)

loop_max:
lb $19, 0($10)
sltu $20, $18, $19
bne $20, $0,  store_data

addi $10, $10, 1
addi $11, $11, -1
bne $11, $0, loop_max

addi $11, $0, 100
addi $10, $0, 0x2020
addi $23, $0, 0x2000
addi $8, $0, 0
beq $0, $0, loop_match

pattern_match:
addi $8, $8, 1
beq $0, $0, else

loop_match:
lb $19, 0($10)
addi $9, $0, 0x1F
and  $20, $19, $9
beq $20, $9, pattern_match

addi $9, $0, 0x3E
and  $20, $19, $9
beq $20, $9, pattern_match

addi $9, $0, 0x7C
and  $20, $19, $9
beq $20, $9, pattern_match

addi $9, $0, 0xF8
and  $20, $19, $9
beq $20, $9, pattern_match

else:
sw $8, 8($23)
addi $10, $10, 1
addi $11, $11, -1
bne $11, $0, loop_match
