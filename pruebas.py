from ctypes import *

class File(Structure):
 _fields_ = [("fileSize", c_uint),
            ("fileName", c_byte * 32)]

f = File()
f.fileSize = 2
print(f.fileSize)
p = pointer(f)
print(p.contents.fileSize)

