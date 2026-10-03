# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import *
import numpy as np

def send_bits(bitstring):
    machine = QMachine()
    machine.init_qvm()
    
    sender = machine.qAlloc()
    receiver = machine.qAlloc()
    c = machine.cAlloc_many(2)
    
    prog = QProg()
    prog.insert(H(sender))
    prog.insert(CNOT(sender, receiver))
    prog.insert(BARRIER([sender, receiver]))
    
    if bitstring[1] == "1":
        prog.insert(Z(sender))
    if bitstring[0] == "1":
        prog.insert(X(sender))
        
    prog.insert(BARRIER([sender, receiver]))
    prog.insert(CNOT(sender, receiver))
    prog.insert(H(sender))
    prog.insert(Measure(sender, c[0]))
    prog.insert(Measure(receiver, c[1]))
    
    return {"prog": prog, "machine": machine, "c": c}
