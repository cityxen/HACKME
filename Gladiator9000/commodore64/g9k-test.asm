////////////////////////////////////////////////////////////////
//  Commodore 64 joystick reading routine
// 
// 2021 CityXen
// 
// UP9600 Driver: $c000
// $dc01 = port 1
// $dc00 = port 2
//
//////////////////////////////////////////////////////////////////////////////////////

.segmentdef up9600

#import "../../Commodore64_Programming/include/Constants.asm"

//////////////////////////////////////////////////////////////////////////////////////
// File stuff
.file [name="g9k-test.prg", segments="Main,up9600"]
.file [name="UP9600.C64", segments="Main"]
.disk [filename="g9k-test.d64", name="CITYXEN G9KTEST", id="2021!" ] {
    [name="G9K-TEST", type="prg",  segments="Main,up9600"],
    [name="UP9600-BASIC.PRG", type="prg", prgFiles="up9600-driver/up9600-basic.prg"],
    [name="UP9600.C64", type="prg", prgFiles="up9600-driver/up9600.bin"]
}

.segment Main [allowOverlap]
*=$0801 "BASIC"
 :BasicUpstart($0815)
*=$080a "cITYxEN wORDS"
.byte $3a,99,67,73,84,89,88,69,78,99
*=$0815 "MAIN PROGRAM"

program:

    // INITIALIZE STUFF
    lda #$00
    sta BACKGROUND_COLOR
    sta BORDER_COLOR
    lda #$93
    jsr KERNAL_CHROUT
    lda #23
    sta $d018 // put to lower case mode
    
    //////////////////////////////////////////////////////////////////////////////////////
    // up9600 initialization
    jsr up9600_load
    jsr $c0fc // init up9600 driver
    bcc rs232found
    ldx #$00 // print message that can't find rs232 user port device
!out:
    lda no_rs232,x
    beq !out+
    jsr KERNAL_CHROUT
    inx
    jmp !out-
!out:
    rts
rs232found:
    jmp main_loop
    rts
    //////////////////////////////////////////////////////////////////////////////////////

no_rs232:
.encoding "petscii_mixed"
.text "Can not find RS-232 userport device"
.byte 0

main_loop:
    jsr up9600_read
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

up9600_read:
    clc
    jsr $c0b9
    bcs !over+
    jsr KERNAL_CHROUT
    jsr $c0dd
!over:
    rts

up9600_load:
    lda #$ba
    ldx #$08
    ldy #$01
    jsr KERNAL_SETLFS
    lda #$0a
    ldx #<up9600_filename
    ldy #>up9600_filename
    jsr KERNAL_SETNAM
    lda #00
    jsr KERNAL_LOAD
    rts
    
up9600_filename:
.encoding "screencode_mixed"
.text "UP9600.C64"
.byte 0
