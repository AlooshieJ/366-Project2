addi $8 , $0 , 0x2000
addi $9, $0 , 1
add $10, $0, $9
addi $19,$0,255
addi $18, $0, 8
addi $17,$0,4
addi $12,$0,0x2000

loop_sb:
sb $10, 0($8)
addi $8, $8 ,1
addi $10, $10, 1
bne $10,$19, loop_sb

sb $10, 0($8)
sb $10, 1($8)

loop_lb:
lb $11,0($8)
addi $15, $0, 0
addi $16, $0, 0

loop_and:
andi $14,$11, 1
beq $14, $9, ones_count
j shift

ones_count:
addi $15,$15, 1

shift:
srl $11, $11, 1
addi $16,$16, 1
bne $16, $18 ,loop_and
bne $15, $17,load_next
addi $20,$20,1

load_next:
addi $8,$8, -1
bne $8 , $12,loop_lb
