.intel_syntax noprefix
.globl _start

.section .data

sockaddr_in:
    .word  2                 # sin_family: AF_INET.
    .word  0x5000            # sin_port: HTTP port (80) in network byte order (big-endian).
    .long  0x0               # sin_addr: 0.0.0.0 (INADDR_ANY).
    .zero  8                 # sin_zero: padding.

request_buffer: .skip 1024   # Allocate 1024 bytes for the request buffer.
http_response:           .asciz "HTTP/1.0 200 OK\r\n\r\n"
file_path:               .skip 256
file_buffer:             .skip 1024
listening_socket_fd:     .quad 0
client_socket_fd:        .quad 0
requested_file_fd:       .quad 0
requested_file_length:   .quad 0

.section .text

_start:
    CREATE_SOCKET:
        mov rax, 41
        mov rdi, 2
        mov rsi, 1
        mov rdx, 0
        syscall

    # Get the socket file descriptor returned by the socket() syscall.
    mov listening_socket_fd, rax

    BIND_SOCKET:
        mov rax, 49
        mov rdi, listening_socket_fd
        lea rsi, [rip + sockaddr_in]
        mov rdx, 16
        syscall

    LISTEN_INCOMING_REQUESTS:
        mov rax, 50
        mov rdi, listening_socket_fd
        mov rsi, 0
        syscall

    SERVER_LOOP:
        ACCEPT_INCOMING_REQUESTS:
            mov rax, 43
            mov rdi, listening_socket_fd
            mov rsi, 0
            mov rdx, 0
            syscall

        # Get the client socket file descriptor returned by the accept() syscall.
        mov client_socket_fd, rax

        FORK:
            mov rax, 57
            syscall
        
        test rax, rax                      # Get the result of fork() syscall.
        je CHILD_PROCESS                   # If rax == 0, this is the child process.
        jl FORK_ERROR                      # If rax < 0, fork failed.

        PARENT_PROCESS:                    # Parent process (rax > 0).
            CLOSE_CLIENT_SOCKET:           # Close the client socket in the parent process.
                mov rax, 3
                mov rdi, client_socket_fd
                syscall
                jmp SERVER_LOOP            # Continue to accept new connections.
        
        CHILD_PROCESS:
            CLOSE_LISTENING_SOCKET:        # Close the listening socket in the child process.
                mov rax, 3
                mov rdi, listening_socket_fd
                syscall

            CLIENT_REQUSET_HANDLER:
                READ_SOCKET:
                    mov rax, 0
                    mov rdi, client_socket_fd
                    lea rsi, [rip + request_buffer]
                    mov rdx, 1024
                    syscall
            
                EXTRACT_PATH:
                    lea rdi, [rip + request_buffer]     # Load the request buffer address into rdi.
                    lea rdx, [rip + file_path]          # Load the file path buffer address into rsi.
                    call EXTRACT_FILE_PATH_GET

                # Check the result.
                test eax, eax                           # Get the result of the EXTRACT_FILE_PATH_GET call.
                jnz EXIT_CHILD_WITH_ERROR               # If eax == 1, handle the not found case.
            
                OPEN_FILE:
                    mov rax, 2
                    lea rdi, [rip + file_path]
                    mov rsi, 0
                    syscall

                # Get the new file descriptor returned by the open() syscall.
                mov requested_file_fd, rax

                READ_FILE:
                    mov rax, 0
                    mov rdi, requested_file_fd
                    lea rsi, [rip + file_path]
                    mov rdx, 1024
                    syscall

                # Get the length of the requested file.
                mov requested_file_length, rax

                CLOSE_FILE:
                    mov rax, 3
                    mov rdi, requested_file_fd
                    syscall
            
                WRITE_SOCKET_RESPONSE_1:
                    mov rax, 1
                    mov rdi, client_socket_fd
                    lea rsi, [rip + http_response]
                    mov rdx, 19
                    syscall

                WRITE_SOCKET_RESPONSE_2:
                    mov rax, 1
                    mov rdi, client_socket_fd
                    lea rsi, [rip + file_path]   
                    mov rdx, requested_file_length
                    syscall
            
                CLOSE_SOCKET:
                    mov rax, 3
                    mov rdi, client_socket_fd
                    syscall
                
                EXIT_CHILD_GRACEFULLY:
                    # Exit the child process gracefully.
                    mov rax, 60
                    mov rdi, 0
                    syscall
                
                EXIT_CHILD_WITH_ERROR:
                    # Exit the child process with error.
                    mov rax, 60
                    mov rdi, 1
                    syscall
    
    FORK_ERROR:
        # Handle fork error
        mov rax, 60              
        mov rdi, 1               # Exit the parent process with error.
        syscall

    EXIT_PARENT:
        # Exit the parent process.
        mov rax, 60
        mov rdi, 0               # Exit the parent process gracefully.
        syscall

    EXTRACT_FILE_PATH_GET:
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
            jmp EXTRACT_FILE_PATH_GET_LOOP

            SKIP_CHAR:
                inc rdi
                jmp FIND_GET_PREFIX

            NOT_FOUND:
                mov eax, 1                            # Set return value to 1 (not found).
                ret                                   # Return if "GET " is not found.
            
        EXTRACT_FILE_PATH_GET_LOOP:
            cmp byte ptr [rdi], ' '
            je EXTRACT_FILE_PATH_GET_END              # If space is found, end of path.
            mov al, [rdi]
            mov [rdx], al
            inc rdi
            inc rdx
            jmp EXTRACT_FILE_PATH_GET_LOOP
        
        EXTRACT_FILE_PATH_GET_END:
            mov byte ptr [rdx], 0                     # Null-terminate the path string.
            mov eax, 0                                # Set return value to 0 (successful).
            ret                                       # Return to the caller.
