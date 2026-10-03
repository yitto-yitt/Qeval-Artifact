# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda

def send_bits(bitstring):
    qvm = pyqpanda.init_quantum_machine(pyqpanda.QMachineType.CPU)
    sender = qvm.qAlloc_many(1)
    receiver = qvm.qAlloc_many(1)
    measure = qvm.cAlloc_many(2)
    
    prog = pyqpanda.QProg()
    prog << pyqpanda.H(sender[0])
    prog << pyqpanda.CNOT(sender[0], receiver[0])
    
    if bitstring[1] == "1":
        prog << pyqpanda.Z(sender[0])
    if bitstring[0] == "1":
        prog << pyqpanda.X(sender[0])
        
    prog << pyqpanda.CNOT(sender[0], receiver[0])
    prog << pyqpanda.H(sender[0])
    
    prog << pyqpanda.Measure(sender[0], measure[0])
    prog << pyqpanda.Measure(receiver[0], measure[1])
    
    return prog
