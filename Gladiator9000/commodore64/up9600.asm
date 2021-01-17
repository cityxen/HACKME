///////////////////////////////////////////////////////////////////////////////////////
// Converted to KickAssembler code January 15, 2021
// By Deadline / CityXen https://youtube.com/cityxen
// 
// Contents:
//
// 1) source code (luna format)
// 2) uuencoded binary
// 3) how to interface with BASIC V2.0
//
// ==============================================================================
// 1) source code
//
//        ;; rewritten (based on LUnix' getty code)
//        ;;  UP9600
//        ;;    (universal) device dirver for RS232 userport interface with
//        ;;    special wiring.
//
//        ;; Nov 23 1997 by Daniel Dallmann
//
//        org $c000
//
//        ;; provided functions
//       
// .global install                 ; install and (probe for) UP9600 (c=error)
// .global enable                  ; (re-)enable interface
// .global disable                 ; disable interface (eg. for floppy accesses)
//
//        ;; rsout and rsin both modify A and X register
//        
// .global rsout                   ; put byte to RS232 (blocking)
// .global rsin                    ; read byte from RS232 (c=try_again)

.file [name="UP9600.C64", segments="Main"]
.disk [filename="UP9600.d64", name="UP9600", id="2021!" ] {
    [name="UP9600-BASIC.PRG", type="prg", prgFiles="up9600-basic.prg"],
    [name="UP9600.C64", type="prg", prgFiles="up9600.bin.orig.prg"],
	[name="UP9600-2.C64", type="prg",  segments="Main"],
}
.segment Main [allowOverlap]
.const jiffies=$a2
.const original_irq=$ea31
.const original_nmi=$fe47
.const nmi_vect=$318
.const irq_vect=$314
// static variables
*=$c20b 
stime: .byte 1 // copy of $a2=jiffies to detect timeouts
outstat: .byte 1 // 
wr_sptr: .byte 1 //  write-pointer into send buffer
rd_sptr: .byte 1 //  read-pointer into send buffer
wr_rptr: .byte 1 //  write-pointer into receive buffer
rd_rptr: .byte 1 //  read-pointer into receive buffer
revtab: .fill 128,0
// .newpage
recbuf: .fill 256,0
sndbuf: .fill 256,0
//.global recbuf, sndbuf

*=$c000
nmi_startbit:
        pha
        bit  $dd0d              // check bit 7 (startbit ?)
        bpl  !nmi_lbl+          // no startbit received, then skip
        
        lda  #$13
        sta  $dd0f              // start timer B (forced reload, signal at PB7)
        sta  $dd0d              // disable timer and FLAG interrupts
        lda  #<nmi_bytrdy       // on next NMI call nmi_bytrdy
        sta  nmi_vect           // (triggered by SDR full)

!nmi_lbl:
        pla                     // ignore, if NMI was triggered by RESTORE-key
        rti

nmi_bytrdy:
        pha
        bit  $dd0d              // check bit 7 (SDR full ?)
        bpl  !nmi_lbl-          // SDR not full, then skip (eg. RESTORE-key)
        
        lda  #$92
        sta  $dd0f              // stop timer B (keep signalling at PB7!)
        sta  $dd0d              // enable FLAG (and timer) interrupts
        lda  #<nmi_startbit     // on next NMI call nmi_startbit
        sta  nmi_vect           // (triggered by a startbit)
        txa
        pha
        lda  $dd0c              // read SDR (bit0=databit7,...,bit7=databit0)
        cmp  #128               // move bit7 into carry-flag
        and  #127
        tax
        lda  revtab,x           // read databits 1-7 from lookup table
        adc  #0                 // add databit0
        ldx  wr_rptr            // and write it into the receive buffer
        sta  recbuf,x
        inx
        stx  wr_rptr
        sec
        txa
        sbc  rd_rptr
        cmp  #200
        bcc  !nmi_lbl+
        lda  $dd01              // more than 200 bytes in the receive buffer
        and  #$fd               // then disbale RTS
        sta  $dd01
!nmi_lbl:
        pla
        tax
        pla
        rti

        // IRQ part

new_irq:  
        lda  $dc0d              // read IRQ-mask
        lsr  //a
        lsr  //a                  // move bit1 into carry-flag (timer B - flag)
        and  #2                 // test bit3 (SDR - flag)
        beq  !nmi_lbl+          // SDR not empty, then skip the first part
        ldx  outstat
        beq  !nmi_lbl+          // skip, if we're not waiting for an empty SDR
        dex
        stx  outstat
        bne  !nmi_lbl+          // skip, if we're not waiting for an empty SDR
        
        php
        jsr  send_nxtbyt        // send the next databyte
        plp
        
!nmi_lbl:
        bcs  !nmi_lbl+          // skip if there was no timer-B-underflow
        jmp  $ea81              // return from IRQ
        
!nmi_lbl:  // keyscan IRQ
        sec                     // (a lost SDR-empty interrupt, would
        lda  jiffies            // totally lock up the sender. So i've added
        sbc  stime              // a timeout)
        cmp  #16                // (timeout after 16/64 = 0.25 seconds)
        bcc  !nmi_lbl+         // no timeout jet
        jsr  send_nxtbyt        // send the next databyte
!nmi_lbl:
        jmp  original_irq

        // send next byte from buffer
send_nxtbyt:        
        lda  jiffies            // remember jiffie counter for detecting
        sta  stime              // timeouts
        lda  $dd01              // check CTS line from RS232 interface
        and  #$40
        beq  !nmi_lbl+          // skip (because CTS is inactive)
        ldx  rd_sptr
        cpx  wr_sptr
        beq  !nmi_lbl+          // skip (because buffer is empty)
        lda  sndbuf,x
        inx
        stx  rd_sptr
        cmp  #128               // move bit7 into carry-flag
        and  #127               // get bits 1-7 from lookup table
        tax
        lda  revtab,x
        adc  #0                 // add bit0
        lsr  //a
        sta  $dc0c              // send startbit (=0) and the first 7 databits
        lda  #2                 // (2 IRQs per byte sent)
        sta  outstat
        ror  //a
        ora  #127               // then send databit7 and 7 stopbits (=1)
        sta  $dc0c              // (and wait for 2 SDR-empty IRQs or a timeout
!nmi_lbl:
        rts                     // before sending the next databyte)
        
        // get byte from serial interface
        
rsin:   ldx  rd_rptr
        cpx  wr_rptr
        beq  !nmi_lbl++                 // skip (empty buffer, return with carry set)
        lda  recbuf,x
        inx
        stx  rd_rptr
        pha
        txa
        sec
        sbc  wr_rptr
        cmp  #256-50
        bcc  !nmi_lbl+
        lda  #2                 // enable RTS if there are less than 50 bytes
        ora  $dd01              // in the receive buffer
        sta  $dd01
        clc
!nmi_lbl:
        pla
!nmi_lbl:
        rts

        // put byte to serial interface
rsout:
        ldx  wr_sptr
        sta  sndbuf,x
        inx
!nmi_lbl:
        cpx  rd_sptr            // wait for free slot in the send buffer
        beq  !nmi_lbl-
        stx  wr_sptr
        lda  outstat
        bne  !nmi_lbl+
        lda  jiffies
        eor  #$80
        sta  stime              // force timeout on next IRQ
!nmi_lbl:
        rts

        // install (and probe for) serial interface
        // return with carry set if there was an error

inst_err:
        cli
        sec
        rts
        
install:  
        sei
        lda  irq_vect
        cmp  #<original_irq
        bne  inst_err           // IRQ-vector already changed 
        lda  irq_vect+1
        cmp  #>original_irq
        bne  inst_err           // IRQ-vector already changed
        lda  nmi_vect
        cmp  #<original_nmi
        bne  inst_err           // NMI-vector already changed 
        lda  nmi_vect+1
        cmp  #>original_nmi
        bne  inst_err           // NMI-vector already changed

        ldy  #0
        sty  wr_sptr
        sty  rd_sptr
        sty  wr_rptr
        sty  rd_rptr
        
        // probe for RS232 interface

        cli
        lda  #$7f
        sta  $dd0d              // disable all NMIs
        lda  #$80
        sta  $dd03              // PB7 used as output
        sta  $dd0e              // stop timerA
        sta  $dd0f              // stop timerB
        bit  $dd0d              // clear pending interrupts
        ldx  #8
!nmi_lbl:
        stx  $dd01              // toggle TXD
        sta  $dd01              // and look if it triggers an
        dex                     // shift-register interrupt
        bne  !nmi_lbl-
        lda  $dd0d              // check for bit3 (SDR-flag)
        and  #8
        beq  inst_err           // no interface detected

        // generate lookup table
        
        ldx  #0
!nmi_lbl:
        stx  outstat            // outstat used as temporary variable
        ldy  #8
!nmi_lbl:
        asl  outstat
        ror  //a
        dey
        bne  !nmi_lbl-
        sta  revtab,x
        inx
        bpl  !nmi_lbl--

        // enable serial interface (IRQ+NMI)
        
enable:
        sei
        ldx  #<new_irq          // install new IRQ-handler
        ldy  #>new_irq
        stx  irq_vect
        sty  irq_vect+1
        
        ldx  #<nmi_startbit     // install new NMI-handler
        ldy  #>nmi_startbit
        stx  nmi_vect
        sty  nmi_vect+1
        
        ldx  $2a6               // PAL or NTSC version ?
        lda  ilotab,x           // (keyscan interrupt once every 1/64 second)
        sta  $dc06              // (sorry this will break code, that uses
        lda  ihitab,x           // the ti$ - variable)
        sta  $dc07              // start value for timer B (of CIA1)
        txa
        asl  //a
        
        eor  #$33               // ** time constant for sender **
        ldx  #0                 // 51 or 55 depending on PAL/NTSC version
        sta  $dc04              // start value for timerA (of CIA1)
        stx  $dc05              // (time is around 1/(2*baudrate) )
        
        asl  //a                  // ** time constant for receiver **
        ora  #1                 // 103 or 111 depending on PAL/NTSC version
        sta  $dd06              // start value for timerB (of CIA2)
        stx  $dd07              // (time is around 1/baudrate )
        
        lda  #$41               // start timerA of CIA1, SP1 used as output
        sta  $dc0e              // generates the sender's bit clock
        lda  #1
        sta  outstat
        sta  $dc0d              // disable timerA (CIA1) interrupt
        sta  $dc0f              // start timerB of CIA1 (generates keyscan IRQ)
        lda  #$92               // stop timerB of CIA2 (enable signal at PB7)
        sta  $dd0f
        lda  #$98
        bit  $dd0d              // clear pending NMIs
        sta  $dd0d              // enable NMI (SDR and FLAG) (CIA2)
        lda  #$8a
        sta  $dc0d              // enable IRQ (timerB and SDR) (CIA1)
        lda  #$ff
        sta  $dd01              // PB0-7 default to 1
        sta  $dc0c              // SP1 defaults to 1
        sec
        lda  wr_rptr
        sbc  rd_rptr
        cmp  #200
        bcs  !nmi_lbl+          // don't enable RTS if rec-buffer is full
        lda  #2                 // enable RTS
        sta  $dd03              // (the RTS line is the only output)
!nmi_lbl:
        cli
        rts

        // table of timer values for PAL and NTSC version
        
ilotab:
        .byte $95
        .byte $25
ihitab: 
        .byte $42
        .byte $40       

        // disable serial interface
disable:  
        sei
        lda  $dd01              // disable RTS
        and  #$fd
        sta  $dd01
        lda  #$7f
        sta  $dd0d              // disable all CIA interrupts
        sta  $dc0d
        lda  #$41               // quick (and dirty) hack to switch back
        sta  $dc05              // to the default CIA1 configuration
        lda  #$81
        sta  $dc0d              // enable timer1 (this is default)

        lda  #<original_irq     // restore old IRQ-handler
        sta  irq_vect
        lda  #>original_irq
        sta  irq_vect+1
        
        lda  #<original_nmi     // restore old NMI-handler
        sta  nmi_vect
        lda  #>original_nmi
        sta  nmi_vect+1
        cli
        rts
/*
==============================================================================
 2) c64-binary (uuencoded)

begin 644 up9600.c64
M`,!(+`W=$`VI$XT/W8T-W:D5C1@#:$!(+`W=$/BIDHT/W8T-W:D`C1@#BDBM
M#-W)@"E_JKT1PFD`K@_"G0##Z(X/PCB*[1#"R<B0"*T!W2G]C0'=:*IH0*T-
MW$I**0+P$*X,PO`+RHX,PM`%"""$P"BP`TR!ZCBEHNT+PLD0D`,@A,!,,>JE
MHHT+PJT!W2E`\"BN#L+L#<+P(+T`Q.B.#L+)@"E_JKT1PFD`2HT,W*D"C0S"
M:@E_C0S<8*X0PNP/PO`;O0##Z(X0PDB*..T/PLG.D`FI`@T!W8T!W1AH8*X-
MPIT`Q.CL#L+P^XX-PJT,PM`'I:))@(T+PF!8.&!XK10#R3'0]:T5`\GJT.ZM
M&`/)1]#GK1D#R?[0X*``C`W"C`["C`_"C!#"6*E_C0W=J8"-`]V-#MV-#]TL
M#=VB"(X!W8T!W<K0]ZT-W2D(\*RB`(X,PJ`(#@S":HC0^9T1PN@0[GBB5J#`
MCA0#C!4#H@"@P(X8`XP9`ZZF`KW6P8T&W+W8P8T'W(H*23.B`(T$W(X%W`H)
M`8T&W8X'W:E!C0[<J0&-#,*-#=R-#]RIDHT/W:F8+`W=C0W=J8J-#=RI_XT!
MW8T,W#BM#\+M$,+)R+`%J0*-`]U88)4E0D!XK0'=*?V-`=VI?XT-W8T-W*E!
>C07<J8&-#=RI,8T4`ZGJC14#J4>-&`.I_HT9`UA@
`
end

==============================================================================
3) how to interface with BASIC V2.0

10 fl=fl+1
20 if fl=1 then load"up9600.c64",8,1
30 sys 49404 : rem install up9600 driver
40 if peek(783)and1 then print "can't detect rs232 interface": end

100 sys 49337
110 if peek(783)and1 goto 100 : rem nothing received jet
120 b=peek(780) : rem b holds the received byte

130 poke 780,b:sys 49373 : rem send byte b
140 goto 100

 you can disable the interface with "sys 49626"
 and enable it again with "sys 49505"
 (a must, when you want to access your floppy or printer!)
*/