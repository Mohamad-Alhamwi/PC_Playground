.intel_syntax noprefix

.section .text

.globl _start
_start:

# Count the consecutive non-zero bytes in a contiguous region of memory, where:
# rdi = memory address of the 1st byte
# rax = number of consecutive non-zero bytes

xor rbx, rbx # counter = 0.
xor rax, rax # rax = 0, number of consecutive non-zero bytes.

cmp rdi, 0
je PROGRAM_END

CONDITION:
mov cl, byte ptr [rdi + rbx]
cmp cl, 0x00
je PROGRAM_END
ja PROGRAM_LOGIC

PROGRAM_LOGIC:
inc rbx
jmp CONDITION

PROGRAM_END:
mov rax, rbx
