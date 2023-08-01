# DinoParkTycoonRipper
A bunch of quick'n'dirty scripts for ripping graphic assets from DinoPark Tycoon (1993)

To rip everything, just run `ripall.sh`. It will automatically rip palettes, pictures and sprites.
`files` is a list of ACT files along with names of palette files it should use.

Please note that this software is just "good enough" for my reasons - i just wanted to know if there are any unused assets.
As such, some pictures don't get ripped for reasons I'm not interested in investigating,
and any of the additional data in ACT files (animation info most likely) isn't read at all.  
Also, a few ACT files are in some other format.

The compression algorithms itself are just simple RLE, I might document them here later.
It shouldn't be too difficult to create a simple encoder.
