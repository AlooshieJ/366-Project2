lui $8, 0xFA19
ori $8, $8, 0xE366
addi $9,$0,1  				
addi $11,$0,100 
lui $13,0xffff
addi $14, $0 ,0x1f 
addi $15,$0,0x2020 
addi $16,$0,0x2000 
addi $18,$0,0	
addi $23, $0 , 5
loop_100:
hash_5:
multu $9 , $8
mfhi $22 
mflo $21 
xor $19, $22,$21
addi $23,$23,-1
hash_4:
multu $19, $8 
mfhi $22 
mflo $21 
xor $19, $22,$21
addi $23,$23,-1 
bne $23, $0, hash_4
j last_fold
out:
sw $10,0($15) 	
sw $18,8($16) 		
addi $15, $15, 4 
addi $9, $9, 1 
addi $11,$11, -1 
addi $23, $0 , 5 
bne $11,$0,loop_100
j end
last_fold:
xor $22,$19, $13 
sll $21, $22,16 
srl $21, $21,16 
xor $22,$22,$13 
srl $20, $22,16 
xor $10,$21,$20
xori $22,$10,0xff00
sll $21, $22, 24
srl $21,$21, 24
xori $22,$22,0xff00
srl $20, $22, 8 
xor $10,$21,$20 
j find_max
find_max:
lw $22, 4($16)
sltu $19,$22,$10  
bne $19,$0,save_max
j pattern_check
save_max:	
sw $10,4($16)
sw $15,0($16)
j pattern_check
pattern_check:
and $22,$10,$14	
bne $22, $14,check_two
j one_count
check_two:
srl $22,$10,1	
and $21,$22,$14 
bne $21, $14,check_3 
j one_count
check_3:
srl $22,$10,2 
and $21,$22,$14
bne $21, $14,check_4
j one_count
check_4:
srl $22,$10,3 
and $21,$22,$14
bne $21, $14,out
one_count:
addi $18, $18, 1 
j out
end:
