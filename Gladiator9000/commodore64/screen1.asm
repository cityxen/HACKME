

// PETSCII memory layout (example for a 40x25 screen)'
// byte  0         = border color'
// byte  1         = background color'
// bytes 2-1001    = screencodes'
// bytes 1002-2001 = color

screen_gladiator9000:
.byte 0,0
.byte 160,236,226,226,226,226,251,160,226,226,251,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160
.byte 236,126,160,160,160,160,124,251,225,160,225,226,226,251,160,160,160,160,160,160,236,226,226,251,236,226,226,251,160,160,160,160,160,160,160,160,160,160,160,160
.byte 126,160,160,108,123,160,160,124,32,32,124,225,160,124,226,226,226,226,226,226,126,160,160,32,32,160,160,225,236,226,226,226,251,236,226,226,226,226,226,251
.byte 245,160,108,254,252,98,98,123,160,160,32,160,160,160,32,160,160,32,160,160,32,160,160,160,118,160,160,124,126,160,160,160,124,126,160,160,160,160,160,124
.byte 245,160,225,160,160,160,160,252,225,160,108,225,160,108,123,160,160,32,160,160,108,123,32,160,160,226,108,123,160,160,32,160,160,32,160,160,160,32,160,246
.byte 245,160,124,251,236,226,226,251,225,160,225,225,160,225,97,160,160,32,160,160,124,126,160,160,160,160,124,126,160,160,160,160,160,32,160,160,108,123,160,246
.byte 123,160,160,124,126,160,160,225,225,160,225,225,160,124,126,160,160,160,160,160,32,160,160,160,118,160,160,160,160,160,160,160,108,123,160,160,225,97,160,246
.byte 252,123,160,160,160,160,108,254,225,160,225,32,160,160,32,32,160,160,160,160,32,160,160,160,160,160,160,32,32,160,160,160,225,97,160,160,225,97,160,246
.byte 160,252,98,98,98,98,254,160,98,98,254,252,98,98,254,97,32,32,160,160,108,98,98,254,252,98,98,254,252,98,98,98,254,252,98,98,254,252,98,98
.byte 160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,97,160,160,160,108,254,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160
.byte 160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,252,98,98,98,254,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160,160
.byte 160,126,32,32,32,32,32,32,32,160,160,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,124,160
.byte 160,32,108,160,160,97,32,252,32,32,32,108,160,123,32,160,160,123,32,160,160,160,126,108,160,123,32,160,160,160,126,108,160,123,32,160,160,252,32,160
.byte 160,32,160,32,32,32,32,160,32,32,32,160,124,160,32,160,124,160,32,32,160,32,32,160,124,160,32,32,160,32,32,160,124,160,32,160,124,160,32,160
.byte 160,32,160,32,160,252,32,160,32,32,32,160,236,160,32,160,32,160,32,32,160,32,32,160,236,160,32,32,160,32,32,160,32,160,32,160,160,126,32,160
.byte 160,32,160,123,108,160,32,160,123,32,32,160,32,160,32,160,123,160,32,32,160,32,32,160,32,160,32,32,160,32,32,160,123,160,32,160,251,252,32,160
.byte 160,32,124,160,160,126,32,124,160,160,32,160,32,160,32,160,160,126,32,160,160,160,32,160,32,160,32,32,160,32,32,124,160,126,32,160,32,160,32,160
.byte 160,123,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,160,32,32,32,32,32,32,32,108,160
.byte 160,160,160,160,160,160,160,236,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,251,160,160,160,160,160,160,160,160
.byte 160,160,160,160,160,160,160,32,98,98,98,98,98,32,98,98,98,98,98,32,98,98,98,98,98,32,98,98,98,98,98,32,160,160,160,160,160,160,160,160
.byte 160,160,160,160,160,160,160,32,160,160,32,32,98,32,98,32,32,32,160,32,98,32,32,32,160,32,98,32,32,160,160,32,160,160,160,160,160,160,160,160
.byte 160,160,160,160,160,160,160,32,160,160,160,160,160,32,160,32,160,32,160,32,160,32,160,32,160,32,160,32,160,160,160,32,160,160,160,160,160,160,160,160
.byte 160,160,160,160,160,160,160,32,226,226,226,226,160,32,160,32,32,32,160,32,160,32,32,32,160,32,160,32,32,160,160,32,160,160,160,160,160,160,160,160
.byte 160,160,160,160,160,160,160,32,32,32,32,32,226,32,226,226,226,226,226,32,226,226,226,226,226,32,226,226,226,226,226,32,160,160,160,178,176,178,177,160
.byte 160,160,160,160,160,160,160,252,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,254,160,160,160,160,160,160,160,160
.byte 3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3
.byte 3,3,1,7,7,7,3,3,1,7,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3
.byte 3,7,7,11,11,7,7,3,7,7,3,1,7,3,3,3,3,3,3,3,3,1,7,7,1,1,7,3,3,3,3,3,3,3,3,3,3,3,3,3
.byte 7,7,11,11,11,11,11,11,7,7,7,7,7,7,7,1,7,7,1,7,7,7,7,7,7,7,7,3,3,1,7,7,3,3,1,7,7,7,7,3
.byte 7,7,11,14,14,11,11,11,7,7,11,7,7,11,11,7,7,14,7,7,11,11,7,7,7,7,11,11,1,7,7,7,7,8,7,7,7,7,7,7
.byte 7,7,11,14,14,14,14,14,7,7,11,7,7,11,11,7,7,7,7,7,11,11,7,7,7,7,11,11,7,7,7,7,7,8,7,7,11,11,7,7
.byte 11,7,7,14,14,7,7,11,7,7,11,7,7,11,11,7,7,0,7,7,7,7,7,7,7,7,7,0,7,7,0,0,11,11,7,7,11,11,7,7
.byte 11,11,7,7,7,7,11,11,7,7,11,7,7,7,7,7,7,7,7,7,7,7,7,0,0,7,7,8,7,7,7,7,11,11,7,7,11,11,7,7
.byte 14,11,11,11,11,11,11,11,14,11,11,14,11,11,11,14,14,8,7,7,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11
.byte 14,14,11,11,11,11,14,14,14,11,11,14,11,11,11,14,7,7,7,11,11,11,11,11,14,11,11,11,14,11,11,11,11,14,11,11,11,14,11,11
.byte 14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,11,11,11,11,11,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14
.byte 14,14,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,15,15,2,2,2,2,2,2,15,15,2,2,2,2,2,2,2,14,14
.byte 6,2,2,2,2,2,2,2,1,2,1,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,6
.byte 6,12,2,12,12,12,12,2,12,12,12,2,2,2,12,2,2,2,12,12,2,12,12,2,2,2,12,2,2,12,12,2,2,2,12,2,2,2,12,6
.byte 6,12,2,12,2,2,12,2,12,12,12,2,2,2,12,2,12,2,12,12,2,12,12,2,2,2,12,2,2,12,12,2,12,2,12,2,2,2,12,6
.byte 6,12,2,2,2,2,12,2,2,12,12,2,12,2,12,2,2,2,12,12,2,12,12,2,12,2,2,2,2,12,12,2,2,2,12,2,2,2,12,6
.byte 6,15,2,2,2,2,2,2,2,2,15,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,15,2,2,2,2,12,2,15,2,2,6
.byte 4,4,15,2,2,2,2,2,4,4,4,4,15,4,4,4,4,4,2,15,15,15,15,15,15,2,2,15,15,2,0,2,15,2,15,15,15,2,4,4
.byte 4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4
.byte 4,4,4,4,4,4,4,12,7,7,7,7,7,12,7,7,7,7,7,12,7,7,7,7,7,12,7,7,7,7,7,4,4,4,4,4,4,4,4,4
.byte 4,4,4,4,4,4,4,12,7,0,12,12,7,12,7,12,12,12,7,12,7,12,12,12,7,12,7,12,12,0,7,12,4,4,4,4,4,4,4,4
.byte 4,4,4,4,4,4,4,12,7,0,0,0,7,12,7,12,7,12,7,12,7,12,7,12,7,12,7,12,7,0,7,12,4,4,4,4,4,4,4,4
.byte 9,9,9,9,9,9,9,12,7,7,7,7,7,12,7,12,12,12,7,12,7,12,12,12,7,12,7,12,12,0,7,12,9,9,9,9,9,9,9,9
.byte 9,9,9,9,9,9,9,9,12,12,12,12,7,12,7,7,7,7,7,12,7,7,7,7,7,12,7,7,7,7,7,12,9,9,9,9,9,9,9,9
.byte 9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9