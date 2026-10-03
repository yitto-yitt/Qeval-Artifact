# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def xor_gate(a, b):
    # Initialize the CPU quantum virtual machine
    machine = CPUQVM()
    machine.init_qvm()
    
    # Allocate 8 qubits and 8 classical bits
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    
    prog = QProg()
    
    # Compute bitwise XOR of a and b
    val = a ^ b
    for i in range(8):
        if (val >> i) & 1:
            prog << X(q[i])
            
    # Measure qubits to corresponding classical bits
    for i in range(8):
        prog << Measure(q[i], c[i])
        
    # Run the program. To match Qiskit's MSB-first (big-endian) representation,
    # we pass the classical bits in reverse order.
    shots = 1000
    counts = machine.run_with_configuration(prog, c[::-1], shots)
    
    # Calculate probabilities
    total = builtins.sum(counts.values())
    result = {key: value / total for key, value in counts.items()}
    
    machine.finalize()
    return result
