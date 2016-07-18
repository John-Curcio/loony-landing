import math
import numpy as np

def conjugate(q): #"conjugate" is a noun, not a verb
    w, x, y, z = q
    return (w, -x, -y, -z)

def normalize(v, tolerance=0.00001): #v must be like an array (tuple, list, whatever)
    mag = np.linalg.norm(v) #magnitude of vector v. 
    if abs(mag - 1.0) > tolerance:
        v = np.asarray(v) / mag
    return v

def mult(q1, q2): 
    #code here looks like a bunch of rats with tails tied together
    #but the derivation isn't so bad
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def mult_qv(q1, v1):
    q2 = (0.0,) + v1
    return mult(mult(q1, q2), conjugate(q1))[1:]

def axisangle_to_q(v, theta):
    v = normalize(v)
    x, y, z = v
    theta /= 2
    w = math.cos(theta)
    x = x * math.sin(theta)
    y = y * math.sin(theta)
    z = z * math.sin(theta)
    return (w, x, y, z)

def axisangle_from_q(q):
    w, v = q[0], q[1:]
    theta = acos(w) * 2.0
    return (normalize(v), theta)



