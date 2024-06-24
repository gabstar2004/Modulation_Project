import numpy as np
import xml.etree.ElementTree as ET

def createLUT(binStrings, coords):
    return dict(zip(binStrings, coords))

# DEFINE PRESET QAM symbol mappings

def createBinStrings(n):
    if n < 0:
        raise ValueError('n needs to be positive')
    bins = []
    for i in range(0, n):
        bins.append(format(i, 'b').zfill(int(np.ceil(np.log2(n)))))
    return bins
  
#QPSK with (1,1) = 11, (-1,1) = 01, (-1,-1) = 00, (1,-1) = 10  
QPSK_I = createLUT(createBinStrings(4), [-1, -1, 1, 1])
QPSK_Q = createLUT(createBinStrings(4), [-1, 1, -1, 1])

QAM16_I = createLUT(createBinStrings(16), [-3,-3,-3,-3,-1,-1,-1,-1,3,3,3,3,1,1,1,1])
QAM16_Q = createLUT(createBinStrings(16), [-3,-1,3,1,-3,-1,3,1,-3,-1,3,1,-3,-1,3,1])

Presets = dict(zip(['QPSK', '16QAM'], [(QPSK_I, QPSK_Q), (QAM16_I, QAM16_Q)]))

def makeIQComponents(Imap, Qmap, file_path):
    f = open(file = file_path, mode = 'rb')
    data = f.read()
    bits = ''.join(f'{byte:08b}' for byte in data)
    
    # M = BAUD RATE
    M = int(np.log2(len(Imap)))
    
    # ADD PADDING
    bits = bits + '0'*(M - len(bits)%M)
    
    I = []
    Q = []
    
    for i in range(0, len(bits), M):
        symbol = bits[i:i+M]
        I.append(Imap[symbol])
        Q.append(Qmap[symbol])
        
    return I, Q

def rotate45(real, imag, num_rotations=0):
    xcoords = []
    ycoords = []
    n = num_rotations % 4
    for i in range(len(real)):
        xcoords.append((real[i] - imag[i])/np.sqrt(2))
        ycoords.append((real[i] + imag[i])/np.sqrt(2))
    if n == 0:
        return xcoords, ycoords
    real = xcoords
    imag = ycoords
    return rotate45(real, imag, n-1)

def customQAM(xml_file, constel_no):
    def toFloat(string):
        return float(string)
    constel = ET.parse(xml_file)
    root = constel.getroot()[0]
    points = list(map(toFloat, root[0].text.split()))
    syms2bit = root[2][constel_no][0].text.split()
    Imap = dict(zip(syms2bit,points[::2]))
    Qmap = dict(zip(syms2bit,points[1::2]))
    return Imap, Qmap

def countConstels(xml_file):
    xml = ET.parse(xml_file)
    return len(xml.getroot()[0][2])

def differentialEncoder(Imap, Qmap):
    def diff(bits):
        newbits = np.zeros(len(bits))
        for i in range(0,len(bits)):
            newbits[i] = (int(bits[i]) + int(newbits[i-1])) % 2
        return ''.join(str(int(bit)) for bit in newbits) 
    
    newIkeys = map(diff, Imap.keys())
    newQkeys = map(diff, Qmap.keys())
    
    return dict(zip(newIkeys, Imap.values())), dict(zip(newQkeys, Qmap.values()))
   
    
    
             
if __name__ == '__main__':
   file_path = "C:/Users/gabie/Downloads/1715721724978_output.bit"
   print(QPSK_I, QPSK_Q)
   print(differentialEncoder(QPSK_I, QPSK_Q))
   




            
