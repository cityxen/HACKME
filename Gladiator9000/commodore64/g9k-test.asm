////////////////////////////////////////////////////////////////
// Gladiator 9000 Client for the Commodore 64
// 
// 2021 Deadline / Xamfear / CityXen
//
// https://linktr.ee/cityxen
// 
// UP9600 Driver: $c000
// 
// $dc01 = port 1
// $dc00 = port 2
//
//////////////////////////////////////////////////////////////////////////////////////
// Initial defines and imports
.segmentdef up9600
#import "../../../Commodore64_Programming/include/Constants.asm"

//////////////////////////////////////////////////////////////////////////////////////
// File stuff
.file [name="g9k-test.prg", segments="Main,up9600"]
.file [name="UP9600.C64", segments="Main"]
.disk [filename="g9k-test.d64", name="CITYXEN G9KTEST", id="2021!" ] {
    [name="G9K-TEST", type="prg",  segments="Main,up9600"],
    [name="UP9600-BASIC.PRG", type="prg", prgFiles="up9600-driver/up9600-basic.prg"],
    [name="UP9600.C64", type="prg", prgFiles="up9600-driver/up9600.bin"]
}

//////////////////////////////////////////////////////////////////////////////////////
// BASIC Upstart stuff
.segment Main [allowOverlap]
*=$0801 "BASIC"
 :BasicUpstart($0815)
*=$080a "cITYxEN wORDS"
.byte $3a,99,67,73,84,89,88,69,78,99
*=$0815 "MAIN PROGRAM"

//////////////////////////////////////////////////////////////////////////////////////
// Program start
program:
    lda #$00 // INITIALIZE STUFF
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
    jsr up9600_zero_read_string // zero read string buffer 
    jmp main_loop
    rts

no_rs232:
.encoding "petscii_mixed"
.text "Can not find RS-232 userport device"
.byte 0
    //////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////
// Main Loop
main_loop:
    jsr up9600_read
    jsr joyport_read 
    jsr to_screen
    jmp main_loop

//////////////////////////////////////////////////////////////////////////////////////
// Joyport read stuff
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

//////////////////////////////////////////////////////////////////////////////////////
// Print Joyport status to screen
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

//////////////////////////////////////////////////////////////////////////////////////
// Joyport data stuff
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

//////////////////////////////////////////////////////////////////////////////////////
// UP9600 write routine
up9600_write:
    ldx #$00
!wl:
    lda up9600_write_string,x
    beq !wl+
    sta up9600_tmp
    txa
    pha
    lda up9600_tmp    
    jsr $c0dd
    pla
    tax
    inx
    jmp !wl-
!wl:
    inc up9600_counter+1    
    lda up9600_counter+1
    cmp #$3a
    bne !wl++
    lda #$30
    sta up9600_counter+1
    inc up9600_counter
!wl:
    lda up9600_counter
    cmp #$3a
    bne !wl+
    lda #$30
    sta up9600_counter
!wl:
    ldx #$00
!wl:
    lda up9600_counter,x
    beq !wl+
    sta up9600_tmp
    txa
    pha
    lda up9600_tmp    
    jsr $c0dd
    pla
    tax
    inx
    jmp !wl-
!wl:
    rts

up9600_write_string:
.text "c64:"
.byte 0
up9600_counter:
.text "00"
.byte 0
up9600_tmp:
.byte 0

//////////////////////////////////////////////////////////////////////////////////////
// UP9600 read / parse routine
up9600_read:
    jsr $c0b9
    bcc !over+
    rts
!over:
    ldx up9600_read_string_cursor // store the string in read string buffer (256 bytes)
    inc up9600_read_string_cursor
    sta up9600_read_string,x    
    cmp #$0d // is the string finished?
    beq up9600_parse
    rts
up9600_parse:
    ldx #$00
!lp:
    lda up9600_read_string,x
    inx
    cpx #up9600_read_string_cursor
    bne !lp-
    jsr KERNAL_CHROUT // test by putting output to screen
    jsr up9600_zero_read_string
    // add parsing here
    rts

up9600_zero_read_string:
    lda #$00
    sta up9600_read_string_cursor
    ldx #$00
!lp:
    sta up9600_read_string,x
    inx
    bne !lp-
    rts

up9600_read_string_cursor:
.byte 0
up9600_read_string:
.fill 256,0

//////////////////////////////////////////////////////////////////////////////////////
// UP9600 load from disk routine
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
