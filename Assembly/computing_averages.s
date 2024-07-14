.intel_syntax noprefix

.section .text

.globl _start
_start:


xor rbx, rbx # sum = 0.
xor rcx, rcx # counter = 0.

BOUNDRY_CHECK:
cmp rcx, rsi # boundary value comparision.
jb  LOOP
jae PROGRAM_END

LOOP:
add rbx, [rdi + rcx * 8]
inc rcx
jmp BOUNDRY_CHECK

PROGRAM_END:
mov rax, rbx
idiv rcx
