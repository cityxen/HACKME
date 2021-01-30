// HYP_R.COM
// 
// Optimized R: handler
// for Multi-I/O and Black Box
// 
// Copyright 1995, 1997 Lenard R. Spencer
// 
// Multi-I/O tm FTe
// Black Box tm CSS
// Atari tm Atari Corporation
// 
// THIS PROGRAM MAY BE FREELY DISTRIBUTED
// BUT MAY NOT BE INCORPORATED INTO ANY
// OTHER SOFTWARE PACKAGE.
// 
// This is a replacement handler for the
// ROM handlers in the Multi-I/O and
// Black Box, in and effort to provide a
// more efficient handler for the newer
// high-speed modems.  The problem is not
// so much the handlers themselves, but
// rather the Atari XL/XE operating
// system, and its overhead of code in
// what is called the "generic handler"
// just to access the ROM handlers.
// There is also an excess of overhead
// code in the interrupt handler just to
// get to the ROM interrupt service
// routines.  This memory-resident
// handler has its own IRQ routine that
// is patched into the IRQ vector at
// $0216, so it can check the hardware
// directly.
// 
// This source code assembles into two
// versions, one for the Multi-I/O, the
// other for the Black Box, depending on
// how the variable MIO is set.  If
// MIO=0, a Black Box version will be
// assembled.  If MIO=non-zero, a MIO
// version will result.
// 
// This handler is optimized for using
// the RS-232 port strictly for modem
// operations, so do not attempt to use
// it for a serial printer or the system
// will lock up.
// 
// Now, ON TO THE CODE!
// 
         .PAGE "HARDWARE CONSTANTS"
// 
BRKKEY   =   $11     // BREAK key flag
ICCOMZ   =   $22     // ZP IOCB COMMAND
ICAX1Z   =   $2A     // ZP IOCB AUX 1
ICAX2Z   =   $2B     // ZP IOCB AUX 2
IRQVEC   =   $0216   // IRQ vector
MEMLO    =   $02E7   // free memory start
DVSTAT   =   $02EA   // device status
// 
// DEVICE REGISTERS AND VARIABLES
// 
// 
// 
MIO      =   1       // 1=MIO, 0=BB
// 
// 
         .IF MIO
ACIAREG    =   $D1C0 // ACIA register
ACIASTAT   =   $D1C1 // ACIA status reg -
                     // DO NOT WRITE!
ACIACOM    =   $D1C2 // ACIA command reg
ACIACTL    =   $D1C3 // ACIA control reg
HWLINES    =   $D1FF // RS232 lines
DTRREG     =   $D1C2 // DTR location
RTSREG     =   $D1C2 // RTS location
DTRMASK    =   $FE   // mask for DTR
RTSMASK    =   $F3   // mask for RTS
CTS        =   $04   // CTS line bit
RTS        =   $08   // RTS enable
DTR        =   $01   // DTR enable
// 
           .ELSE 
ACIAREG    =   $D130 // ACIA register
ACIASTAT   =   $D131 // ACIA status reg -
           //          DO NOT WRITE!
ACIACOM    =   $D132 // ACIA command reg
ACIACTL    =   $D133 // ACIA control reg
HWLINES    =   $D1C0
DTRREG     =   $D1BF // DTR location
RTSREG     =   $D1BD // RTS location
DTRMASK    =   $F7   // mask for DTR
RTSMASK    =   $F7   // mask for RTS
CTS        =   $40   // CTS line bit
RTS        =   $08   // RTS enable
DTR        =   $08   // DTR enable
           .ENDIF 
// 
         *=  $4000   // To be relocated
START    //            Needed by relocator
// 
         .PAGE "INTERRUPT ROUTINE"
// 
IRQ      PHA         // save accum.,X
         TXA 
         LDX ACIASTAT // ACIA IRQ?
         BMI IRQ2    // yes - skip
         TAX 
         PLA 
SYSIRQ   JMP $C030   // otherwise out
IRQ2     PHA 
         TYA 
         PHA 
         TXA         // get status
         AND #8      // receive?
         BEQ TRYSEND // no - try send
W01      LDY LASTIN
         LDA ACIAREG // get byte
W02      STA INBUFF,Y // store it
         INY 
W03      STY LASTIN
W04      CPY NEXTIN  // rolled over?
         BNE TRYSEND // no - go to send
W05      INC NEXTIN  // else set flag
W06      LDA STATERR //  for buffer
         ORA #$10    //   overflow
W07      STA STATERR
TRYSEND  TXA 
         AND #$10    // Tx reg empty?
         BEQ IRQEXIT //  
         LDA ACIACOM // Tx enabled?
         AND #$0C
         CMP #4
         BNE IRQEXIT // no - exit
SEND02   LDA HWLINES // CTS monitoring
         AND #CTS    // CTS = 1?
         BEQ IRQEXIT // no - bail out
W09      LDY NEXTOUT
W10      CPY LASTOUT // buffer empty?
         BNE SENDIT  // no - send byte
W11      JSR DSTXIRQ // disable Tx IRQ
IRQEXIT  PLA         // restore regs
         TAY 
         PLA 
         TAX 
         PLA 
         RTI         // bail out!
SENDIT   INY 
W12      LDA OUTBUFF,Y
         STA ACIAREG
W13      STY NEXTOUT
W14      JMP IRQEXIT
DSTXIRQ  LDA #8
         .BYTE $2C   // imp. BIT inst.
ENTXIRQ  LDA #4
         EOR ACIACOM
         AND #$0C
         EOR ACIACOM
         STA ACIACOM
         RTS 
// 
         .PAGE "GET BYTE ROUTINE"
// 
GET      BIT BRKKEY  // BREAK key pressed?
         BPL GET10   // yes - bail out!
W15      LDX NEXTIN  // get pointer
W16      CPX LASTIN  // buffer empty?
         BEQ GET     // yes - loop back
W17      LDY INBUFF,X // get byte
         INX         // bump pointer
W18      STX NEXTIN  // save it
W19      LDA TRANS
         AND #$20    // ATASCII?
         BNE GET10   // yes - skip
         CPY #$0D    // ASCII CR?
         BNE GET10   // no - skip
         LDY #$9B    // make ATASCII EOL
         BNE GET10
W20      LDA TRANS
         AND #$10
         BEQ GET10
         TYA 
         AND #$7F
         TAY 
         CPY #$7D
         BCS GET08
         CPY #$20
         BCS GET10
W21
GET08    LDY TCHR
GET10    TYA 
W22      JMP SETBREAK
// 
         .PAGE "PUT BYTE, SET BREAK"
// 
PUT      TAY 
W23      LDA TRANS
         AND #$20    // ATASCII?
         BNE PUT03   // yes - skip
         CPY #$9B    // ATASCII EOL?
         BNE PUT03   // no - skip
         LDY #$0D    // else make CR
W24      JSR PUT10   // send it
W25      BIT TRANS   // need LF?
         BVC SETBREAK // no - skip
         LDY #$0A    // else send LF
W26
PUT03    JSR PUT10   // send character
SETBREAK LDY #1      // assume OK
         BIT BRKKEY  // BREAK pressed?
         BMI SETEXIT // no - skip
         LDY #$80    // else ERROR 128
         STY BRKKEY  // reset BREAK flag
SETEXIT  CPY #0      // set exit flags
         SEC         // yes we handled it
         RTS 
W27
PUT10    LDX LASTOUT // get pointer
         INX 
PUT11    BIT BRKKEY  // BREAK pressed?
         BPL PUTEXIT // yes - bail out
W28      CPX NEXTOUT // buffer full?
         BEQ PUT11   // yes - loop back
         SEI 
         TYA 
W29      STA OUTBUFF,X // put in buffer
W30      STX LASTOUT // save pointer
W31      JSR ENTXIRQ // enable Tx IRQ
         CLI 
PUTEXIT  RTS 
// 
         .PAGE "OPEN, CLOSE R: CHANNEL"
// 
OPEN     LDA ICAX1Z  // get aux 1 byte
         AND #$0C
W32      STA MODE    // save
         SEI 
         LDX #5
         LDA #0      // zero out working
W33
OP01     STA STATERR,X //  variables
         DEX 
         BPL OP01
OP02     CLI 
W35
OPEN03   LDA MODE
         STA ICAX1Z
W36      JMP SETBREAK
// 
//  CLOSE R: HANDLER CHANNEL
// 
CLOSE    LDA #0      // end concurrent
W37      STA CONCUR  //   mode
W38
XIO32    LDA LASTOUT // get pointer
F01      BIT BRKKEY  // BREAK pressed?
         BPL F02     // yes - exit
W39      CMP NEXTOUT // buffer empty?
         BNE F01     // no - loop back
W40
F02      JMP OPEN03  // exit
// 
         .PAGE "GET STATUS OF R: CHANNEL"
// 
STATUS   LDA HWLINES // read H/S lines
         .IF MIO=0
           LSR A
           LSR A
           LSR A
           LSR A
           LSR A
           .ENDIF 
         AND #7      // get index
         TAX         //  index
W43      LDA HSFLAGS,X
W44      ORA HSLAST
         STA DVSTAT+1
         AND #$A8
         LSR A
W45      STA HSLAST
W46      BIT CONCUR  // concurrent mode?
         BPL STAT02  // no - skip
         SEC 
W47      LDA LASTIN  // calc bytes in
W48      SBC NEXTIN  //  input buffer
         STA DVSTAT+1
         SEC 
W49      LDA LASTOUT // calc bytes in
W50      SBC NEXTOUT //  output buffer
         STA DVSTAT+3
W51
STAT02   LDA STATERR // status flags
         STA DVSTAT
         LDA #0      // clear flags
W52      STA STATERR
         STA DVSTAT+2
W53      JMP SETBREAK
HSFLAGS  .IF MIO
           .BYTE $01,$09,$81,$89
           .BYTE $21,$29,$A1,$A9
           .ELSE 
           .BYTE $01,$81,$21,$A1
           .BYTE $09,$89,$29,$A9
           .ENDIF 
// 
         .PAGE "XIO 40, 38, 36 CALLS"
// 
SPECIAL  LDX ICCOMZ  // get command
         LDA ICAX1Z  // get aux 1
         CPX #$28    // set concurrent?
         BNE XIO38   // no - try next
W54      LDA CONCUR  // set flag for
         ORA #$80    //  concurrent mode
W55      STA CONCUR  //   operation
W56      JMP OPEN03
XIO38    CPX #$26    // trans, parity?
         BNE XIO36   // no - try next
W57      STA TRANS   // save directly
         LSR A
         LSR A
         AND #3      // get parity bits
         TAY 
         LDA ACIACOM
         AND #$1F
W58      ORA PARITY,Y
         STA ACIACOM
         LDA $2B
W59      STA TCHR
W60      JMP OPEN03
PARITY   .BYTE 0,$20,$60,$A0
XIO36    CPX #$24    // baud, word size?
         BNE XIO34   // no - try next
         TAY         // temp save
         AND #$D0    // set word size,
         ASL A       //  stop bits
         PHP 
         ASL A
         PLP 
         ROR A
         PHA         // temp save
         TYA 
         AND #$0F    // get baud rate
         BEQ XIO36C  // 0 = 300 baud
         LDX #8
         CMP #5      // 110 baud?
         BEQ XIO36A  // yes - skip down
         SEC         // otherwise -
         CMP #8      //  standard rates?
         BCC ERR132  // no - error out
         AND #7      // get index
XIO36C   TAX 
XIO36A   PLA         // retrieve byte
W61      ORA BAUD,X  // index baud table
         STA ACIACTL
W63
XIO36B   JMP OPEN03
BAUD     .BYTE $16,$17,$18,$19
         .BYTE $1A,$1C,$1E,$1F,$13
         .PAGE "ERROR 132//  XIO 34, 32"
W64
ERR132   JSR SETBREAK
         TYA 
         BMI ER132A
         LDY #$84    // illegal XIO call
ER132A   RTS 
XIO34    CPX #$22    // set H/S lines?
         BNE XIO32A  // no - skip
         TAX 
         BIT ICAX1Z  // set DTR?
         BPL XIO34A  // no - skip
         PHP 
         LDA DTRREG
         AND #DTRMASK
         .IF MIO=0
           ORA #$34
           .ENDIF 
         PLP 
         BVC XIO34B
         ORA #DTR    // set DTR true
XIO34B   STA DTRREG
XIO34A   TXA 
         AND #$20    // set RTS?
         BEQ XIO34C  // no - skip
         TXA 
         AND #$10
         PHP 
         LDA RTSREG
         AND #RTSMASK
         .IF MIO=0
           ORA #$34
           .ENDIF 
         PLP 
         BEQ XIO34D
         ORA #RTS
XIO34D   STA RTSREG
XIO34C   TXA 
         AND #2      // set XMT?
         BEQ X34F    // no - exit
         TXA 
         AND #1
         PHP 
         LDA ACIACOM
         AND #$F3
         ORA #8
         PLP 
         BEQ XIO34E
         ORA #4
XIO34E   STA ACIACOM
W65
X34F     JMP OPEN03
XIO32A   CPX #$20    // XIO 32?
         BNE ERR132  // no - error out
W66      JMP XIO32
         .PAGE "RESET INITIALIZATION"
INIT     JSR $FFFF   // DOSINI vector
L01
INIT02   LDA # <RELOC // move MEMLO up to
         STA MEMLO   //  protect handler
H01      LDA # >RELOC
         STA MEMLO+1
         LDX #0
INIT03   LDA $031A,X // find handler
         BEQ SETHAND // end of HATABS
         CMP #$52    // "R:"
         BEQ SET02   // R: handler found
         INX 
         INX 
         INX 
         BNE INIT03
SETHAND  LDA #$52
         STA $031A,X
L02
SET02    LDA # <HATAB
         STA $031B,X
H02      LDA # >HATAB
         STA $031C,X
         LDA IRQVEC  // patch into
W67      STA SYSIRQ+1 //  IRQ vector
         LDA IRQVEC+1
W68      STA SYSIRQ+2
         SEI 
L03      LDA # <IRQ
         STA IRQVEC
H03      LDA # >IRQ
         STA IRQVEC+1
         CLI 
         .IF MIO
           LDA ACIACOM
           AND #$FC
           STA ACIACOM
           .ELSE 
           LDA ACIACOM
           ORA #1
           AND #$FD
           STA ACIACOM
           LDA #$34  // set DTR low
           STA DTRREG
           .ENDIF 
INOUT    RTS 
// 
W69
HATAB    .WORD OPEN-1
W70      .WORD CLOSE-1
W71      .WORD GET-1
W72      .WORD PUT-1
W73      .WORD STATUS-1
W74      .WORD SPECIAL-1
         .BYTE 0
STATERR  .BYTE 0     // status/error fl.
NEXTIN   .BYTE 0     // next byte in
LASTIN   .BYTE 0     // last byte in
NEXTOUT  .BYTE 0     // next byte out
LASTOUT  .BYTE 0     // last byte out
CONCUR   .BYTE 0     // concurrent flag
MODE     .BYTE 0     // I/O mode
TRANS    .BYTE 0     // translation
TCHR     .BYTE 0     // trans character
HSLAST   .BYTE 0     // last H/S states
INBUFF   *=    *+256
OUTBUFF  *=    *+256
         .PAGE "GENERIC RELOCATOR"
// GENERIC RELOCATOR - written for use
//  with other programs as well.
// 
RELOC    LDX #0      // Just to make sure
REL01    LDA $031A,X // we have room in
         BEQ REL01A  // the handler table
         INX 
         INX 
         INX 
         CPX #$21
         BCC REL01
         LDA # <ERRMSG
         LDX # >ERRMSG
         LDY #ERREND-ERRMSG
REL01A   LDA # <START // calculate
         SEC         //  offset for
         SBC MEMLO   //   relocation
         STA OFFSET
         LDA # >START
         SBC MEMLO+1
         STA OFFSET+1
         LDX #0      // initialize for
         LDY #0      //  relocation loop
REL02    LDA TABLO,X
         STA $E0
REL03    LDA TABHI,X
         STA $E2
         INX 
REL04    LDA TABLO,X
         STA $E1
REL05    LDA TABHI,X
         STA $E3
         ORA $E2     // end of table?
         BEQ MOVEIT  // yes - drop down
         LDA ($E0),Y // else - recalc
         SEC         //  address
         SBC OFFSET
         STA ($E0),Y
         LDA ($E2),Y
         SBC OFFSET+1
         STA ($E2),Y
         INX         // next address
         BNE REL02   // no wrap - go back
         INC REL02+2 // else bump
         INC REL03+2 //  addresses up
         INC REL04+2 //   to next page
         INC REL05+2
         JMP REL02
         .PAGE "MOVE CODE TO MEMLO"
MOVEIT   LDA # <START // move handler
         STA $E0     //  to MEMLO
         LDA # >START
         STA $E1
         LDA MEMLO
         STA $E2
         LDA MEMLO+1
         STA $E3
         LDA # <RELOC-START
         STA $E4
         LDA # >RELOC-START
         STA $E5
MOVE02   LDA ($E0),Y
         STA ($E2),Y
         INC $E0
         BNE MOVE03
         INC $E1
MOVE03   INC $E2
         BNE MOVE04
         INC $E3
MOVE04   LDA $E4
         BNE MOVE05
         DEC $E5
MOVE05   DEC $E4
         BNE MOVE02
         LDA $E5
         BNE MOVE02
RELINIT  LDA $0C     // DOSINI vector
M06      STA INIT+1  //  patch point
         LDA $0D
M07      STA INIT+2
M08      LDA # <INIT
         STA $0C
M09      LDA # >INIT
         STA $0D
M10      JSR INIT02
PRTMSG   LDA # <MSG
         LDX # >MSG
         LDY # <MSGEND-MSG
PRTERR   STA $0344
         STX $0345
         STY $0348
         LDA #11
         STA $0342
         LDX #0
         STX $0349
         JMP $E456
         .PAGE "COPYRIGHT NOTICE"
MSG      .BYTE "HyperSpeed RS232 "
         .BYTE "accelerator",$9B
         .BYTE "Version 1.3a FREEWARE" 
         .IF MIO
           .BYTE " for Multi I/O"
           .ELSE 
           .BYTE " for Black Box"
           .ENDIF 
         .BYTE $9B,"Copyright 1995, "
         .BYTE "1997",$9B
         .BYTE "Lenard R. Spencer",$9B
MSGEND
ERRMSG   .BYTE "
Handler table full!",$9B
         .BYTE "HyperSpeed not installed!"
         .BYTE $FD,$9B
ERREND
OFFSET   .WORD 0
         .PAGE "RELOCATOR TABLE 1"
// 
// Each TABLO entry MUST have a matching
// TABHI entry.  TABLO is for the low
// bytes to be offset, TABHI is for the
// high bytes.  TABHI MUST END WITH ZERO
// OR THE RELOCATOR WILL NOT KNOW WHEN
// TO STOP!
// 
TABLO    .WORD M06+1,M07+1,M08+1,M10+1
         .WORD W01+1,W02+1,W03+1,W04+1
         .WORD W05+1,W06+1,W07+1
         .WORD W09+1,W10+1,W11+1,W12+1
         .WORD W13+1,W14+1,W15+1,W16+1
         .WORD W17+1,W18+1,W19+1,W20+1
         .WORD W21+1,W22+1,W23+1,W24+1
         .WORD W25+1,W26+1,W27+1,W28+1
         .WORD W29+1,W30+1,W31+1,W32+1
         .WORD W33+1,W35+1,W36+1
         .WORD W37+1,W38+1,W39+1,W40+1
         .WORD W43+1,W44+1
         .WORD W45+1,W46+1,W47+1,W48+1
         .WORD W49+1,W50+1,W51+1,W52+1
         .WORD W53+1,W54+1,W55+1,W56+1
         .WORD W57+1,W58+1,W59+1,W60+1
         .WORD W61+1,W63+1,W64+1
         .WORD W65+1,W66+1,W67+1,W68+1
         .WORD W69,W70,W71,W72,W73,W74
         .WORD L01+1,L02+1,L03+1
         .PAGE "RELOCATOR TABLE 2"
TABHI    .WORD M06+2,M07+2,M09+1,M10+2
         .WORD W01+2,W02+2,W03+2,W04+2
         .WORD W05+2,W06+2,W07+2
         .WORD W09+2,W10+2,W11+2,W12+2
         .WORD W13+2,W14+2,W15+2,W16+2
         .WORD W17+2,W18+2,W19+2,W20+2
         .WORD W21+2,W22+2,W23+2,W24+2
         .WORD W25+2,W26+2,W27+2,W28+2
         .WORD W29+2,W30+2,W31+2,W32+2
         .WORD W33+2,W35+2,W36+2
         .WORD W37+2,W38+2,W39+2,W40+2
         .WORD W43+2,W44+2
         .WORD W45+2,W46+2,W47+2,W48+2
         .WORD W49+2,W50+2,W51+2,W52+2
         .WORD W53+2,W54+2,W55+2,W56+2
         .WORD W57+2,W58+2,W59+2,W60+2
         .WORD W61+2,W63+2,W64+2
         .WORD W65+2,W66+2,W67+2,W68+2
         .WORD W69+1,W70+1,W71+1,W72+1
         .WORD W73+1,W74+1,H01+1,H02+1
         .WORD H03+1
         .WORD 0     // STOP HERE!
// 
         *=  $02E0   // run address
         .WORD RELOC
         .END 
