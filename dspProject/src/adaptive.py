import numpy as np

def lms_filter(desired, reference, mu=0.01, order=8):
    N = len(desired)
    y = np.zeros(N)
    e = np.zeros(N)
    w = np.zeros(order)
    ref_buf = np.zeros(order)
    for n in range(N):
        ref_buf[1:] = ref_buf[:-1]
        ref_buf[0] = reference[n] if n < len(reference) else 0
        y[n] = np.dot(w, ref_buf)
        e[n] = desired[n] - y[n]
        w += 2 * mu * e[n] * ref_buf
    return e 