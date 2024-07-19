.intel_syntax noprefix

.section .text

.globl _start
_start:

MOST_COMMON_BYTE:
    # param 1 - rdi: src_addr.
    # param 2 - rsi: size.

    # Function prologue.
    push rbp                              # Push current base pointer onto the stack.
    mov rbp, rsp                          # Set up the base of the stack as the current top.
    sub rsp, 0x200                        # Allocate 512 bytes for the frequency table (256 entries, 2 bytes each).

    xor rdx, rdx                          # Set up.
    lea rdx, [rbp - 0x200]                # Get the base address of the frequency table.

    # Zero out the frequency table.
    xor rcx, rcx                          # Set the loop counter to 0.
    ZERO_FREQ_TABLE:
      mov word ptr [rdx + rcx * 2], 0
      inc rcx
      cmp rcx, 0x100
      jne ZERO_FREQ_TABLE

    xor rax, rax                          # Set up rax to conduct math calculations.
    xor rcx, rcx                          # Set the loop counter to 0.
    
    FREQUNECY_CALCULATING_WHILE:
      cmp rcx, rsi                        # (i < size).
      jge END_CALCULATING
      mov al, byte ptr [rdi + rcx]        # Get Current byte.
      inc word ptr [rdx + rax * 2]        # Update frequency table ([base_addr + curr_byte * 2] += 1).
      inc rcx                             # Update the loop counter. 
      jmp FREQUNECY_CALCULATING_WHILE

    END_CALCULATING:
    xor rax, rax                          # Set up rax to conduct math calculations.
    lea rdx, [rbp - 0x200]                # Get the base address of the frequency table.
    xor rcx, rcx                          # Set the loop counter to 0 (b = 0).      
    xor rbx, rbx                          # Set up rbx to hold the maximum frequency (max_freq = 0).
    xor r15, r15                          # Set up r15 to hold the byte with maximum frequency (max_freq_byte = 0).

    MAX_CALCULATING_WHILE:
      cmp rcx, 0x100                      
      jge END
      mov ax, word ptr [rdx + rcx * 2]    # Get frequency of current byte.
      cmp rax, rbx                        # Compare with the current max frequency.
      jle CONTINUE
      mov rbx, rax                        # Update max frequency.
      mov r15, rcx                        # Save the byte with max frequency.

      CONTINUE:
      inc rcx                             # Update the loop counter.
      jmp MAX_CALCULATING_WHILE

    END:
      # Function epilogue.
      mov rsp, rbp                        # Restore the allocated space.
      pop	rbp
      mov rax, r15                        # Return the most common byte.
      ret
