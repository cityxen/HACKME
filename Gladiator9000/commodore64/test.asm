//////////////////////////////////////////////////////////////////////////////////////
// RS-232 Test by Deadline
// KickAssembler RS-232 test
//////////////////////////////////////////////////////////////////////////////////////
// 
// History:
// 
// January 15, 2021:
//      - Started
//
//////////////////////////////////////////////////////////////////////////////////////
#import "../../Commodore64_Programming/include/Constants.asm"
.segment Sprites [allowOverlap]
// Leave out clicky stuff for now 
//*=$2000 "CLICKY EYES"
//#import "Clicky_Eyes_Defs.asm"
//#import "Clicky_Eyes_Data.asm"
//*=$3000 "CLICKY MOUTHS"
//#import "Clicky_Mouths_Data.asm"
//#import "Clicky_Decorations_Data.asm"
//////////////////////////////////////////////////////////////////////////////////////
// File stuff
.file [name="g9k.prg", segments="Main,Sprites"]
.file [name="COMMLIB2.BIN", type="prg", segments="CommLib2" ]
.disk [filename="g9k.d64", name="CITYXEN G9K", id="2021!" ] {
	[name="G9K", type="prg",  segments="Main,Sprites"],
    [name="COMMLIB2.BIN", type="prg", segments="CommLib2" ],
}

//////////////////////////////////////////////////////////////////////////////////////
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
    rts

.segment CommLib2 [allowOverlap]
*=$CA00 "COMMLIB2"
//.var data = LoadBinary("commlib2/commlib2.bin") // Load the file into the variable ’data’
//myData: .fill data.getSize(), data.get(i) // Dump the data to the memory
.import binary "commlib2/commlib2.bin"
