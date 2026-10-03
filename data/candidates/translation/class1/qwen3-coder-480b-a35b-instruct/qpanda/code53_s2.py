# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *
from pyqpanda3.utils import *

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    # Create 9 qubits (8 for data + 1 ancilla)
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(8)
    
    # Initialize circuit
    prog = pq.QProg()
    
    # Apply X gates to set initial state based on 'a'
    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(qubits[i])
    
    # Apply XOR with 'b' - this means flipping bits where b has 1s
    for i in range(8):
        if (b >> i) & 1:
            prog << pq.X(qubits[i])
    
    # Measure all 8 data qubits
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])
    
    # Run the program
    result = machine.run(prog)
    
    # Extract results and calculate probabilities
    counts = {}
    for i in range(len(result)):
        bit_str = ""
        for j in range(7, -1, -1):  # Reverse order to get MSB first
            bit_str += str(result[i][cbits[j]])
        
        if bit_str in counts:
            counts[bit_str] += 1
        else:
            counts[bit_str] = 1
    
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    machine.finalize()
    
    return prob_dist
