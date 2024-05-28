### some routines to convert dpt into hex bytes



def encode_dpt9 (state): # 2byte signed float

   sign = 0x8000 if (state <0) else 0
   exp  = 0
   mant = 0

   mant = int(state * 100.0)
   while (abs(mant) > 2047):
        mant /= 2
        exp += 1

   data = sign | (exp << 11) | (int(mant) & 0x07ff)

   high = "0x"+"%x" % (data >> 8)
   low = "0x"+"%x"% (data & 0xff)

   retval=[high,low]

   return (retval)

def encode_dpt7 (state): # 2byte unsigned int
   high = "%x" % (state >> 8)
   low = "%x"% (state & 0xff)
   retval=[high,low]
   return (retval)

def encode_dpt1(state):  # 1 bit status (0 or 1)

        retval = [hex(state)]
        return retval

def encode_dpt5(state):  # 8 bit unsigned (0..255)
        retval = [hex(state)]
        return retval

