addi $3,$0,1
addi $2,$0,0
addi $5,$0,10

sb $3,0x2000($2)
lb $4,0x2000($2)

loop:
addi $2,$2,1
addi $3,$3,1
addi $5,$5,-1
sb $3,0x2000($2)
beq $0,$0, loop
