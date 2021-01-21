////////////////////////////////////////////////////////////////
//  Commodore 64 joystick reading routine
// 
// $dc01 = port 1
// $dc00 = port 2

#import "../../Commodore64_Programming/include/Constants.asm"

//////////////////////////////////////////////////////////////////////////////////////
// File stuff
.file [name="g9k-jst.prg", segments="Main"]
.disk [filename="g9k-jst.d64", name="CITYXEN G9KJST", id="2021!" ] {
	[name="G9K-JST", type="prg",  segments="Main"]
}

.segment Main [allowOverlap]
*=$0801 "BASIC"
 :BasicUpstart($0815)
*=$080a "cITYxEN wORDS"
.byte $3a,99,67,73,84,89,88,69,78,99
*=$0815 "MAIN PROGRAM"

program:
    lda #$00
    sta BACKGROUND_COLOR
    sta BORDER_COLOR
    lda #$93
    jsr KERNAL_CHROUT
    jmp main_loop
    rts

main_loop:
    jsr joyport_read 
    jsr to_screen
    jmp main_loop

joyport_read:

    lda #$00
    ldx #$00
jprl1:
    sta up1,x
    inx
    cpx #$0a
    bne jprl1

    lda $dc01
    and #$1f
    lsr
    ror up1
    lsr
    ror down1
    lsr
    ror left1
    lsr
    ror right1
    lsr
    ror button1
    lda $dc00
    and #$1f
    lsr
    ror up2
    lsr
    ror down2
    lsr
    ror left2
    lsr
    ror right2
    lsr
    ror button2
    rts

to_screen:
    ldx #$00
tslp:
    lda up1,x
    bne ts1
    adc #$31
    jmp ts2
ts1:
    lda #$30
ts2:
    sta $0400,x
    inx
    cpx #$0a
    bne tslp
    rts

up1:     .byte 0
down1:   .byte 0
left1:   .byte 0
right1:  .byte 0
button1: .byte 0

up2:     .byte 0
down2:   .byte 0
left2:   .byte 0
right2:  .byte 0
button2: .byte 0

