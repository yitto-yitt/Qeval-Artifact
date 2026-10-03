# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, H, X, Z, CNOT, Measure

def send_bits(bitstring):
    qm = QuantumMachine()
    sender = qm.qAlloc(1)
    receiver = qm.qAlloc(1)
    measure = qm.cAlloc(2)
    
    prog = QProg()
    prog << H(sender[0])
    prog << CNOT(sender[0], receiver[0])
    
    if bitstring[1] == "1":
        prog << Z(sender[0])
    if bitstring[0] == "1":
        prog << X(sender[0])
        
    prog << CNOT(sender[0], receiver[0])
    prog << H(sender[0])
    
    prog << Measure(sender[0], measure[0])
    prog << Measure(receiver[0], measure[1])
    
    return prog
