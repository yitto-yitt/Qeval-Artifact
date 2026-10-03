# EVAL_META: task_id=52, framework=qpanda, class=1
import pyqpanda3.core as pq


def send_bits(bitstring):
    machine = pq.QMachine()
    sender = machine.qAlloc()
    receiver = machine.qAlloc()
    c = [machine.cAlloc() for _ in range(2)]
    
    prog = pq.QProg()
    prog.insert(pq.H(sender))
    prog.insert(pq.CNOT(sender, receiver))
    prog.insert(pq.Barrier())
    
    if bitstring[1] == "1":
        prog.insert(pq.Z(sender))
    if bitstring[0] == "1":
        prog.insert(pq.X(sender))
        
    prog.insert(pq.Barrier())
    prog.insert(pq.CNOT(sender, receiver))
    prog.insert(pq.H(sender))
    prog.insert(pq.Measure(sender, c[0]))
    prog.insert(pq.Measure(receiver, c[1]))
    
    return prog
