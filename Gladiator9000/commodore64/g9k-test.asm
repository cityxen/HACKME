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
// From https://github.com/cityxen/Commodore64_Programming
// git clone https://github.com/cityxen/Commodore64_Programming
#import "../../../Commodore64_Programming/include/Constants.asm"
#import "../../../Commodore64_Programming/include/DrawPetMateScreen.asm"

//////////////////////////////////////////////////////////////////////////////////////
// File stuff
.file [name="g9k-test.prg", segments="Main"]
.file [name="UP9600.C64", prgFiles="up9600-driver/up9600.bin"]
.disk [filename="g9k-test.d64", name="CITYXEN G9KTEST", id="2021!" ] {
    [name="G9K-TEST", type="prg",  segments="Main"],
    [name="UP9600-BASIC.PRG", type="prg", prgFiles="up9600-driver/up9600-basic.prg"],
    [name="UP9600.C64", type="prg", prgFiles="up9600-driver/up9600.bin"]
}

//////////////////////////////////////////////////////////////////////////////////////
// BASIC Upstart stuff
.segment Main [allowOverlap]
*=$0801 "BASIC"
 :BasicUpstart($082a)
*=$080a "CityXen Magic Word Stuff" // :(REM TOKEN)(DELx14)2021 cityxen
.byte $3a,$8F,$14,$14,$14,$14,$14,$14,$14,$14,$14,$14,$14,$14,$14,$14,$32,$30,$32,$31,32,67,73,84,89,88,69,78
*=$082a "MAIN PROGRAM"

//////////////////////////////////////////////////////////////////////////////////////
// Program start
program:
    ldx #$f0
!downprt:
    lda #$0d
    jsr KERNAL_CHROUT
    inx
    bne !downprt-
    DrawPetMateScreen(screen_gladiator9000)
    //////////////////////////////////////////////////////////////////////////////////////
    // up9600 initialization
    lda #$ff
    sta $c000
    jsr up9600_load
    lda $c000
    cmp #$ff
    bne good_load
bad_load:
    lda #>badload_txt
    sta zp_tmp_hi
    lda #<badload_txt
    sta zp_tmp_lo
    jsr zprint
    rts // exit program
good_load:
    lda #>goodload_txt
    sta zp_tmp_hi
    lda #<goodload_txt
    sta zp_tmp_lo
    jsr zprint
up9600_init:
    jsr $c0fc // init up9600 driver
    bcc rs232_found
rs232_not_found:
    lda #>no_rs232_txt
    sta zp_tmp_hi
    lda #<no_rs232_txt
    sta zp_tmp_lo
    jsr zprint
    rts // exit program
rs232_found:
    jsr zero_strbuf // zero read string buffer 
    lda #>listening_txt
    sta zp_tmp_hi
    lda #<listening_txt
    sta zp_tmp_lo
    jsr zprint

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
    lda #$20
!lp:
    sta $040a,x
    inx
    cpx #$1d
    bne !lp-

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
// UP9600 read
up9600_read:
    jsr $c0b9
    bcc !over+
    rts
!over:
    ldx buf_crsr 
    sta strbuf,x // store the string in read string buffer (256 bytes)
    inc buf_crsr
    cmp #$0d
    beq up9600_tx_echo
    cmp #$0a
    beq up9600_tx_echo
    rts

up9600_tx_echo:
    // add check here for echo enabled
    // jsr up9600_write_strbuf

up9600_local_echo:
    // add check here for local echo enabled
    ldx #$00
!lp:
    lda strbuf,x
    jsr KERNAL_CHROUT
    inx
    cpx buf_crsr
    bne !lp-
    // fall through

//////////////////////////////////////////////////////////////////////////////////////
// UP9600 parse (first character will direct what to do)
up9600_parse: 
    lda strbuf
    ////////////////////////////////////////////////
    // I (identify string sent)
    cmp #$69 
    bne !np+
    lda #>up9600_ident // send ident string
    sta zp_tmp_hi
    lda #<up9600_ident
    sta zp_tmp_lo
    jsr up9600_write
    jmp parse_end
    ////////////////////////////////////////////////
    // r
!np:
    cmp #$52 // r (ring)
    bne !np+
!np:
parse_end:
    jsr zero_strbuf // zero string buffer
    rts

//////////////////////////////////////////////////////////////////////////////////////
// UP9600 write routine (uses zero page pointer to string which you have to set up prior to calling)
up9600_write_strbuf:
    lda #>strbuf
    sta zp_tmp_hi
    lda #<strbuf
    sta zp_tmp_lo
    // fall through
up9600_write:
!wl:
    ldx #$00
    lda (zp_tmp,x)
    beq !wl+ // TODO: could cause crash if all things are non-zero
    jsr $c0dd
    inc zp_tmp_lo
    jmp !wl-
!wl:
    rts
up9600_write_counter:
    lda #> up9600_counter
    sta zp_tmp_hi
    lda #< up9600_counter
    sta zp_tmp_lo
    jsr up9600_write    
    rts

//////////////////////////////////////////////////////////////////////////////////////
// UP9600 increment counter
up9600_increment_counter:
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
    rts

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

//////////////////////////////////////////////////////////////////////////////////////
// Print HEX representation of a byte. usage: lda #$15;  jsr print_hex
print_hex:
    pha
    pha
    lsr
    lsr
    lsr
    lsr
    tax
    lda print_hex_conv_table,x
    jsr KERNAL_CHROUT
    pla
    and #$0f
    tax
    lda print_hex_conv_table,x
    jsr KERNAL_CHROUT
    pla
    rts

//////////////////////////////////////////////////////////////////////////////////////
// zprint routine (zero page zp_tmp_hi, zp_tmp_lo must be set to point to proper string)
zprint:
    ldx #$00
!wl:
    lda (zp_tmp,x)
    beq !wl+
    jsr $ffd2
    inc zp_tmp_lo
    jmp !wl-
!wl:
    rts

//////////////////////////////////////////////////////////////////////////////////////
// Zero tmp string buffer
zero_strbuf:
    lda #$00
    ldx #$00
!lp:
    sta strbuf,x
    inx
    bne !lp-
    stx buf_crsr
    rts

//////////////////////////////////////////////////////////////////////////////////////
// Data storage, words and stuff
no_rs232_txt:
.encoding "petscii_mixed"
.byte $0d,$1c,$12,$96,$0e
.text "ERROR: Can not find RS-232 UP9600 device"
.byte $0d,$9a,$00
badload_txt:
.byte $0d,$1c,$12,$96,$0e
.text "ERROR: Could not load UP9600.C64 file   "
.byte $0d,$9a,$00
goodload_txt:
.byte $0d,$12,$1e,$0e,$99
.text "INIT: Loaded up9600.c64 file            "
.byte $00
listening_txt:
.byte $12,$1e,$0e,$99
.text "INIT: Listening on UP9600 device        "
.byte $0d,$9a,$00
up9600_filename:
.encoding "screencode_mixed"
.text "UP9600.C64"
.byte 0
print_hex_conv_table:
.byte $30,$31,$32,$33,$34,$35,$36,$37,$38,$39,$41,$42,$43,$44,$45,$46
//////////////////////////////////////////////////////////////////////////////////////
// UP9600 data stuff
up9600_ident: 
.encoding "ascii" // "screencode_mixed" "petscii_mixed" "screencode_lower" "petscii_lower"
.text "IDENTIFY:C64"
.byte 0
up9600_write_string:
.text "c64:"
.byte 0
up9600_counter:
.text "00"
.byte 0
up9600_tmp:
.byte 0
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
// Generic temporary 256 byte String terminated by zero data area
strbuf:
.fill 256,0
buf_crsr:
.byte 0
*=$2000
#import "screen1.asm"