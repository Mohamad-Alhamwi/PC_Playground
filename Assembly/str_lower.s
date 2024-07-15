.intel_syntax noprefix

.section .text

.globl _start
_start:

STR_LOWER:
    xor  rcx, rcx                  # For debuggin purposes.
    xor  r15, r15                  # Initilize the counter to zero.
    xor  r14, r14                  # Set up r14.
    mov  r14, rdi                  # Back up src_addr's value. 
    test rdi, rdi                  # Check if src_addr is NULL.
    jz END                         # If src_addr is 0, jump to END.

START_WHILE:
    xor  rax, rax                  # Set up rax.
    mov  dil, byte ptr [r14]        # Set foo's argument.
    mov  cl,  byte ptr [r14]        # For debuggin purposes.
    test dil, dil                  # Check if the byte is the null terminator.
    jz END                         # if so, jump to END.

    cmp dil, 0x5a                  # Compare the byte with 0x5a ('Z').
    ja NEXT                        # If the byte is greater than 'Z', skip to the next char.

    # Call foo if the byte is <= 'Z'
    mov rdx, 0x403000
    call rdx                       # Call foo
    mov byte ptr [r14], al         # Store the result back to [src_addr].
    mov cl, byte ptr [r14]         # For debuggin purposes.
    inc r15                        # Increment the conversion counter.

NEXT:
    inc r14             # Move to the next byte.
    jmp START_WHILE     # Back to the loop.

END:
    mov rax, r15
    ret
