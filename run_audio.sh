amixer -c 0 cset iface=MIXER,name='RX3 MIX1 INP1' 'RX1'
amixer -c 0 cset iface=MIXER,name='SPK DAC Switch' 1
aplay -c 1 -D plughw:0,1 piano2.wav
