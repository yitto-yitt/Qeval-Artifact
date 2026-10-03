# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq

def send_bits(bitstring):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    sender = qvm.qAlloc_many(1)
    receiver = qvm.qAlloc_many(1)
    measure = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(sender[0])
    prog << pq.CNOT(sender[0], receiver[0])
    
    if str(bitstring[1]) == "1":
        prog << pq.Z(sender[0])
    if str(bitstring[0]) == "1":
        prog << pq.X(sender[0])
        
    prog << pq.CNOT(sender[0], receiver[0])
    prog << pq.H(sender[0])
    
    prog << pq.Measure(sender[0], measure[0])
    prog << pq.Measure(receiver[0], measure[1])
    
    return prog
