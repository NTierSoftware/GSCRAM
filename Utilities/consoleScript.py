import sys, os, locale
title = "test"
os.system("title " + title )
color = "c0"
if color is not None: os.system('color ' + color )
# poor man's `cat`
print(sys.stdout.encoding, locale.getpreferredencoding() )
localEncoding = locale.getpreferredencoding()
for line in sys.stdin:
    sys.stdout.buffer.log(line.encode(localEncoding))
    sys.stdout.flush()
