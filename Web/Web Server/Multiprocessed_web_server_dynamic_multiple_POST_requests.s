.intel_syntax noprefix
.globl _start

.section .data

sockaddr_in:
    .word  2                 # sin_family: AF_INET.
    .word  0x5000            # sin_port: HTTP port (80) in network byte order (big-endian).
    .long  0x0               # sin_addr: 0.0.0.0 (INADDR_ANY).
    .zero  8                 # sin_zero: padding.

request_buffer:          .skip 1024
http_response:           .asciz "HTTP/1.0 200 OK\r\n\r\n"
file_path:               .skip 256
body_buffer:             .skip 1024
file_buffer:             .skip 1024
listening_socket_fd:     .quad 0
client_socket_fd:        .quad 0
requested_file_fd:       .quad 0
requested_file_length:   .quad 0
body_size:               .quad 0

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
            
            # Extract the reqested file path from the request.
            lea rdi, [rip + request_buffer]
            lea rdx, [rip + file_path]
            call EXTRACT_FILE_PATH_POST

            # Check the result.
            test eax, eax                       # Get the result of the EXTRACT_FILE_PATH_POST call.
            jnz EXIT_CHILD_WITH_ERROR           # If eax == 1, handle the not found case.

            # Extract the payload size from the request.
            lea rdi, [rip + request_buffer]
            call EXTRACT_PAYLOAD_SIZE

            # Check the result.
            test eax, eax                       # Get the result of the EXTRACT_PAYLOAD_SIZE call.
            jnz EXIT_CHILD_WITH_ERROR           # If eax == 1, handle the not found case.

            # Extract the body payload.
            lea rdi, [rip + body_buffer]
            lea rsi, [rip + request_buffer]
            lea rdx, [rip + body_size]
            call EXTRACT_PAYLOAD
            
            # Check the result.
            test eax, eax                       # Get the result of the EXTRACT_PAYLOAD call.
            jnz EXIT_CHILD_WITH_ERROR           # If eax == 1, handle the not found case.

            # If eax == 0, proceed with further processing.
            OPEN_FILE:
                mov rax, 2
                lea rdi, [rip + file_path]
                mov rsi, 0x41                   # Flags: O_WRONLY | O_CREAT (0x1 | 0x40 = 0x41).
                mov rdx, 511                    # Mode: 0777 (octal, can also use decimal 511).
                syscall

            # Get the new file descriptor returned by the open() syscall.
            mov requested_file_fd, rax

            WRITE_PAYLOAD_TO__FILE:
                mov rax, 1
                mov rdi, requested_file_fd
                lea rsi, [rip + body_buffer]
                mov rdx, body_size
                syscall

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
                lea rsi, [rip + body_buffer]
                mov rdx, body_size
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

    EXTRACT_FILE_PATH_POST:
        FIND_POST_PREFIX:
            cmp byte ptr [rdi], 'P'
            jne SKIP_CHAR
            cmp byte ptr [rdi + 1], 'O'
            jne SKIP_CHAR
            cmp byte ptr [rdi + 2], 'S'
            jne SKIP_CHAR
            cmp byte ptr [rdi + 3], 'T'
            jne SKIP_CHAR
            cmp byte ptr [rdi + 4], ' '
            jne SKIP_CHAR
            add rdi, 5              # Move rdi past "POST ".
            jmp EXTRACT_FILE_PATH_POST_LOOP

        SKIP_CHAR:
            inc rdi
            jmp FIND_POST_PREFIX

        NOT_FOUND:
            mov eax, 1              # Set return value to 1 (not found).
            ret                     # Return if "POST " is not found.

        EXTRACT_FILE_PATH_POST_LOOP:
            cmp byte ptr [rdi], ' '
            je EXTRACT_FILE_PATH_POST_END          # If space is found, end of path.
            mov al, [rdi]
            mov [rdx], al
            inc rdi
            inc rdx
            jmp EXTRACT_FILE_PATH_POST_LOOP

        EXTRACT_FILE_PATH_POST_END:
            mov byte ptr [rdx], 0   # Null-terminate the path string.
            mov eax, 0              # Set return value to 0 (successful).
            ret                     # Return to the caller.

    EXTRACT_PAYLOAD_SIZE:
        FIND_CONTENT_LENGTH:
            cmp byte ptr [rdi], 'C'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 1], 'o'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 2], 'n'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 3], 't'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 4], 'e'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 5], 'n'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 6], 't'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 7], '-'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 8], 'L'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 9], 'e'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 10], 'n'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 11], 'g'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 12], 't'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 13], 'h'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 14], ':'
            jne SKIP_CHARACTER
            cmp byte ptr [rdi + 15], ' '
            jne SKIP_CHARACTER
            add rdi, 16             # Move rdi past "Content-Length: ".
            jmp EXTRACT_SIZE

        SKIP_CHARACTER:
            inc rdi
            jmp FIND_CONTENT_LENGTH

        PAYLOAD_NOT_FOUND:
            mov eax, 1              # Set return value to 1 (not found).
            ret                     # Return if "Content-Length" is not found.

        EXTRACT_SIZE:
            xor rax, rax                # Clear rax.
            xor rbx, rbx                # Clear rbx.

            EXTRACT_DIGIT:
                cmp byte ptr [rdi], 13  # Check for carriage return (end of number).
                je SIZE_END
                mov bl, [rdi]
                sub bl, '0'             # Convert ASCII to integer.
                imul rax, rax, 10
                add rax, rbx
                inc rdi
                jmp EXTRACT_DIGIT
            
            SIZE_END:
                mov [body_size], rax
                mov eax, 0              # Set return value to 0 (successful).
                ret                     # Return to the caller.
    
    EXTRACT_PAYLOAD:
        FIND_BODY:
            cmp byte ptr [rsi], 13
            jne SKIP_BODY_CHAR
            cmp byte ptr [rsi + 1], 10
            jne SKIP_BODY_CHAR
            cmp byte ptr [rsi + 2], 13
            jne SKIP_BODY_CHAR
            cmp byte ptr [rsi + 3], 10
            jne SKIP_BODY_CHAR
            add rsi, 4              # Move rsi past the "\r\n\r\n".
            jmp EXTRACT_BODY

        SKIP_BODY_CHAR:
            inc rsi
            jmp FIND_BODY

        NOT_FOUND_BODY:
            mov eax, 1              # Set return value to 1 (not found).
            ret                     # Return if body is not found.

        EXTRACT_BODY:
            mov rcx, [rdx]               # Load body size into rcx
            cmp rcx, 0
            jz EXTRACT_PAYLOAD_END    # If rcx = 0, end extraction
            rep movsb                 # Move bytes from [rsi] to [rdi] (rcx times)

        EXTRACT_PAYLOAD_END:
            mov byte ptr [rdi], 0     # Null-terminate the payload.
            mov eax, 0                # Set return value to 0 (successful)
            ret                       # Return to the caller
