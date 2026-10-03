# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def send_bits(bitstring):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    cbit = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    
    # Create Bell pair
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Barrier()
    
    # Apply operations based on bitstring
    if bitstring[1] == "1":
        prog << pq.Z(qubits[0])
    if bitstring[0] == "1":
        prog << pq.X(qubits[0])
    
    prog << pq.Barrier()
    
    # Decode
    prog << pq.CNOT(qubits[0], qubits[1]) << pq.H(qubits[0])
    
    # Measure
    prog << pq.Measure(qubits[0], cbit[0]) << pq.Measure(qubits[1], cbit[1])
    
    return prog
