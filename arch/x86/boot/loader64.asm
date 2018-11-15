[ORG 0x00]
[BITS 16]
section .text

loader16_start:
	mov ax, 0x0800
	mov ds, ax
	mov es, ax

loader16_a20_enable:
	mov ax, 0x2401
	int 0x15
	jc .with_scp

	jmp loader16_protected_mode_enable
.with_scp:
	in al, 0x92
	or al, 0x02
	and al, 0xFE
	out 0x92, al

loader16_protected_mode_enable:
	cli
	lgdt [loader32_gdtr]

	mov eax, cr0
	and eax, 0x7FFFFFFF
	or eax, 0x00000001
	mov cr0, eax

	jmp dword 0x00000008:(loader32_start + 0x8000)

[BITS 32]
loader32_start:
	mov ax, 0x0010
	mov ds, ax
	mov fs, ax
	mov gs, ax

loader32_stack_initialize:
	mov ax, 0x0010
	mov ss, ax

	mov ebp, 0x8000
	mov esp, 0x8000

loader32_wait:
	jmp $

loader32_gdtr:
	dw loader32_gdt_end - loader32_gdt - 1
	dd loader32_gdt + 0x8000

loader32_gdt:
	dw 0x0000	; Null
	dw 0x0000
	db 0x00
	db 0x00
	db 0x00
	db 0x00

	dw 0xFFFF 	; Code
	dw 0x0000
	db 0x00
	db 0x9A
	db 0xCF
	db 0x00

	dw 0xFFFF 	; Data
	dw 0x0000
	db 0x00
	db 0x92
	db 0xCF
	db 0x00
loader32_gdt_end: