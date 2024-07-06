.intel_syntax noprefix
.globl _start

.section .bss

request_buffer:
    .skip 1024                # Allocate 1024 bytes for the request buffer.

.section .data

sockaddr_in:
    .word  2                 # sin_family: AF_INET.
    .word  0x5000            # sin_port: HTTP port (80) in network byte order (big-endian).
    .long  0x0               # sin_addr: 0.0.0.0 (INADDR_ANY).
    .zero  8                 # sin_zero: padding.

http_response:
    .asciz "HTTP/1.0 200 OK\r\n\r\n"

file_path:
    .skip 256

file_buffer:
    .skip 1024 

.section .text
_start:

CREATE_SOCKET:
    mov rax, 41
    mov rdi, 2
    mov rsi, 1
    mov rdx, 0
    syscall

# Get the socket file descriptor returned by the socket() syscall.
mov r11, rax

BIND_SOCKET:
    mov rax, 49
    mov rdi, r11
    lea rsi, [rip + sockaddr_in]
    mov rdx, 16
    syscall

LISTEN_INCOMING_REQUESTS:
    mov rax, 50
    mov rsi, 0
    syscall

ACCEPT_INCOMING_REQUESTS:
    mov rax, 43
    mov rsi, 0
    mov rdx, 0
    syscall

# Get the new socket file descriptor returned by the accept() syscall.
mov r12, rax

READ_SOCKET:
    mov rax, 0
    mov rdi, r12
    lea rsi, [rip + request_buffer]
    mov rdx, 1024
    syscall

EXTRACT_PATH:
    lea rdi, [rip + request_buffer]     # Load the request buffer address into rdi.
    mov r14, rdi                        # Back up the request buffer address.
    lea rdx, [rip + file_path]          # Load the file path buffer address into rsi.
    mov r15, rdx                        # Back up the file path buffer address.

    FIND_GET_PREFIX:
        cmp byte ptr [rdi], 'G'
        jne SKIP_CHAR
        cmp byte ptr [rdi + 1], 'E'
        jne SKIP_CHAR
        cmp byte ptr [rdi + 2], 'T'
        jne SKIP_CHAR
        cmp byte ptr [rdi + 3], ' '
        jne SKIP_CHAR
        add rdi, 4              # Move rdi past "GET ".
        jmp EXTRACT_LOOP

    SKIP_CHAR:
        inc rdi
        jmp FIND_GET_PREFIX

    jmp EXIT                    # If "GET " not found, exit.

    EXTRACT_LOOP:
        cmp byte ptr [rdi], ' '
        je EXTRACT_END          # If space is found, end of path.
        mov al, [rdi]
        mov [rdx], al
        inc rdi
        inc rdx
        jmp EXTRACT_LOOP

    EXTRACT_END:
        mov byte ptr [rdx], 0       # Null-terminate the path string.

OPEN_FILE:
    mov rax, 2
    mov rdi, r15
    mov rsi, 0
    syscall

# Get the new file descriptor returned by the open() syscall.
mov r13, rax

READ_FILE:
    mov rax, 0
    mov rdi, r13
    mov rsi, r15
    mov rdx, 1024
    syscall

# Get the length of the file.
mov r13, rax

CLOSE_FILE:
    mov rax, 3
    syscall

WRITE_SOCKET_RESPONSE_1:
    mov rax, 1
    mov rdi, r12
    lea rsi, [rip + http_response]
    mov rdx, 19
    syscall

WRITE_SOCKET_RESPONSE_2:
    mov rax, 1
    mov rsi, r15     
    mov rdx, r13
    syscall

CLOSE_SOCKET:
    mov rax, 3
    syscall

EXIT:
    mov rax, 60
    mov rdi, 0
    syscall
