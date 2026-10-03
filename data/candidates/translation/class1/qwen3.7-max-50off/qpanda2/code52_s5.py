# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq

def send_bits(bitstring):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    sender = qvm.qAlloc()
    receiver = qvm.qAlloc()
    measure = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(sender)
    prog << pq.CNOT(sender, receiver)
    
    if bitstring[1] == "1":
        prog << pq.Z(sender)
    if bitstring[0] == "1":
        prog << pq.X(sender)
        
    prog << pq.CNOT(sender, receiver)
    prog << pq.H(sender)
    
    prog << pq.Measure(sender, measure[0])
    prog << pq.Measure(receiver, measure[1])
    
    return prog
