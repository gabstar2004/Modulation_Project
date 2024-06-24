import LUT
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from scipy.fft import fft, ifft, rfft

def rrcosFilter(L, alpha, num_taps):
    t = np.arange(num_taps) - (num_taps-1)//2
    h = np.zeros(num_taps)
    
    pi = np.pi
    sqrtL = np.sqrt(L)
    
    h[t==0] = 1/sqrtL*(1-alpha+4*alpha/pi)
    
    spec_ind = np.abs(t) == L/(4*alpha)
    h[spec_ind] = alpha/np.sqrt(2*L)*((1 + 2/pi)*np.sin(pi/(4*alpha)) + (1-2/pi)*np.cos(pi/(4*alpha)))
    
    gen_ind = ~(t==0) & ~(spec_ind)
    n =  t[gen_ind]
    nL = n/L
    nL2 = (4*alpha*nL)**2
    numerator =  1/sqrtL*(np.sin(pi*(1-alpha)*nL) + 4*alpha*nL*np.cos(pi*(1+alpha)*nL))
    denominator = pi*nL*(1-nL2)
    h[gen_ind] = numerator/denominator
    return h
            
def pulseShape(signal, L, alpha, rrcos):
    n = len(signal)
    if L - int(L) == 0:
        L=int(L)
        upsampled = np.zeros((n-1)*(L-1) + n)
        upsampled[::L] = signal
    return sig.fftconvolve(upsampled, rrcos, 'same')

def createWaveform(file_path, Imap, Qmap, L, freq, alpha=1):
    I,Q = LUT.makeIQComponents(Imap, Qmap, file_path)
    n = len(I)
    L=int(L)
    h = rrcosFilter(L, alpha, (n-1)*(L-1) + n)
    Iwave = pulseShape(I, L, alpha,h)
    Qwave = pulseShape(Q, L, alpha,h)
    freq = freq/len(Iwave)
    t = np.arange(0, len(Iwave))
    real = Iwave*np.sqrt(2)*np.cos(2*np.pi*freq*t) - Qwave*np.sqrt(2)*np.sin(2*np.pi*freq*t)
    imag = Iwave*np.sqrt(2)*np.sin(2*np.pi*freq*t) + Qwave*np.sqrt(2)*np.cos(2*np.pi*freq*t)
    return real, imag


def saveSignal(file_name, I, Q, bits = 32, real = True, MSBF = False, signed = True):
    r_or_c = 'f'
    endian = '>'
    bits = bits//8
    if not real:
        r_or_c = 'c'
        I = I + 1j*Q
        bits = bits*2
    if not MSBF:
        endian = '<'
    
    type_string = endian + r_or_c + str(bits)
    dtype = np.dtype(type_string)
    I.astype(dtype).tofile(file_name)
    
    
if __name__ == '__main__':
    file_path = "C:/Users/gabie/Downloads/1715721724978_output.bit"
    
    w=createWaveform(file_path, LUT.QPSK_I, LUT.QPSK_Q, 8,0, 1)[0]
    x=createWaveform(file_path, LUT.QPSK_I, LUT.QPSK_Q, 8,0, 1)[1]
    saveSignal('test', w,x, 16, False, False, True)
    plt.plot(w[0:8000])
#x =createWaveform(file_path, LUT.QPSK_I, LUT.QPSK_Q, 4,-5000)[0]
#print(w[0:200] - x[0:200])
#plt.plot(abs(rfft(w))**2)

#t=np.arange(0,2,0.001)
#print(t)
#l = rfft(np.cos(30*np.pi*t)) #+ np.cos(2*np.pi*9*t))
#plt.plot(t, np.cos(5*np.pi*t))
#plt.plot(l)
#plt.plot(ifft(l))



