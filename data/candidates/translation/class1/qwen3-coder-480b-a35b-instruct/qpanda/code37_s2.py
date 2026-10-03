# EVAL_META: task_id=37, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
from pyqpanda3.utils import *

def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    
    q = qvm.qAlloc_many(n + 1)
    c = qvm.cAlloc_many(n)
    
    prog = QProg()
    
    # Initialize ancilla qubit to |1>
    prog << X(q[n])
    
    # Apply Hadamard to all qubits
    for i in range(n + 1):
        prog << H(q[i])
    
    # Apply controlled-X gates based on secret string s
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[n])
    
    # Apply Hadamard to first n qubits
    for i in range(n):
        prog << H(q[i])
    
    # Measure first n qubits
    for i in range(n):
        prog << Measure(q[i], c[i])
    
    result = qvm.run_with_configuration(prog, c, 1)
    bitstrings = []
    for res in result:
        bitstring = ""
        for i in range(n):
            bitstring += str(res[str(c[i])])
        bitstrings.append(bitstring)
    
    qvm.finalize()
    return [bitstrings, result]
