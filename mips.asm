addi $5,$12,-4
add $2,$4,$zero
L1:
add $1,$0,$8
add $7,$7,$8
addi $3,$3,-2
addi $2,$5,-1
addiu $6,$5,12

multu $2,$4
beq $4,$2,L1




mult $2,$4
srl $5,$4,3
TEST:
lb $3,10($5)
sb $6,100($4)
lw $6,100($4)
sw $6,100($4)
bne $4,$2,TEST
slt $4,$2,$1
sltu $4,$2,$1
and $4,$5,$2
mflo $3
mfhi $3
and $3,$20,$2
xor $2,$4 ,$14
mflo $15
ori $2,$23,3
