[ORG 0x00]
[BITS 16]
section .text

jmp word 0x07C0:bootloader16_start

bootloader16_start:
	mov ax, 0x07C0
	mov ds, ax
	mov ax, 0xB800
	mov es, ax

	mov si, 0

	mov ah, 0x01
	mov ch, 0x3F
	int 0x10

bootloader16_screen_clear:
	mov byte[es:si], 0
	mov byte[es:si + 1], 0x07
	add si, 2

	cmp si, 80 * 25 * 2
	jl bootloader16_screen_clear

bootloader16_disk_initialize:
	mov si, bootloader16_message_failed_to_initialize_disk
	mov ax, 0
	mov dx, 0
	int 0x13
	jc bootloader16_error

bootloader16_disk_read:
	mov si, bootloader16_message_failed_to_read_disk
	mov ax, 0x0800
	mov es, ax
	mov bx, 0x0000

	mov ah, 0x02
	mov al, 0x01
	mov ch, 0x00
	mov dx, 0x00
.loop:
	mov cl, byte[bootloader16_variable_sector]
	int 0x13
	jc bootloader16_error
	add byte[bootloader16_variable_sector], 1

	add bx, 512

	cmp byte[bootloader16_variable_sector], 10
	je bootloader16_loader_run

	jmp .loop

bootloader16_loader_run:
	;jmp word 0x0000:0x8000
	jmp $

bootloader16_error:
	mov ax, 0xB800
	mov es, ax

	mov di, 0
.loop:
	lodsb
	or al, al
	jz .loop_end

	mov byte[es:di], al
	add di, 2
	jmp .loop
.loop_end:
	jmp $

bootloader16_message_failed_to_initialize_disk: db "[setaria] Failed to initialize disk.", 0
bootloader16_message_failed_to_read_disk: db "[setaria] Failed to read disk.", 0
bootloader16_variable_sector: db 2

times 510 - ($ - $$) db 0x00
db 0x55
db 0xAA