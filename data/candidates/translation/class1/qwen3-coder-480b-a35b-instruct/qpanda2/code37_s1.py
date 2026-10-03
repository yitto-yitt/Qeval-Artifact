# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np
from pyqpanda import *
import builtins


def bv_algorithm(s):
    n = len(s)
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    
    prog = QProg()
    
    # Initialize ancilla qubit to |1>
    prog << X(q[n])
    
    # Apply Hadamard to all qubits
    for i in range(n + 1):
        prog << H(q[i])
    
    # Apply CNOT gates based on the secret string s
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[n])
    
    # Apply Hadamard to the first n qubits
    for i in range(n):
        prog << H(q[i])
    
    # Measure the first n qubits
    for i in range(n):
        prog << Measure(q[i], c[i])
    
    result = machine.run(prog, c, shots=1)
    
    # Extract bitstrings from the result
    bitstrings = []
    for key in result.keys():
        bitstring = key
        bitstrings.append(bitstring)
    
    return [bitstrings, result]
