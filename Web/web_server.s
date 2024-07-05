.intel_syntax noprefix
.globl _start

.section .data

sockaddr_in:
    .word  2                 # sin_family: AF_INET.
    .word  0x5000            # sin_port: HTTP port (80) in network byte order (big-endian).
    .long  0x0               # sin_addr: 0.0.0.0 (INADDR_ANY).
    .zero  8                 # sin_zero: padding.


.section .text
_start:

SOCKET_SYS_CALL:
    mov rax, 41
    mov rdi, 2
    mov rsi, 1
    mov rdx, 0

    syscall

# Get the file descriptor returned by syscall.
mov r11, rax

BIND_SYS_CALL:
    mov rax, 49
    mov rdi, r11
    lea rsi, [rip + sockaddr_in]
    mov rdx, 16

    syscall

LISTEN_SYS_CALL:
    mov rax, 50
    mov rsi, 0

    syscall

ACCEPT_SYS_CALL:
    mov rax, 43
    mov rsi, 0
    mov rdx, 0

    syscall

# Get the new file descriptor returned by accept.
mov r12, rax

EXIT_SYS_CALL:
    mov rdi, 0
    mov rax, 60     # SYS_exit
    syscall