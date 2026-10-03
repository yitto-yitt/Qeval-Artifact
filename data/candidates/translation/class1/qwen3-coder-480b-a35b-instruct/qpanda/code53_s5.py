# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *
from pyqpanda3.extensions import *

def xor_gate(a, b):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    # Apply X gates based on bits set in 'a'
    for i in range(8):
        if (a >> i) & 1:
            machine << X(qubits[i])
    
    # Apply X gates based on bits set in 'b'  
    for i in range(8):
        if (b >> i) & 1:
            machine << X(qubits[i])
    
    # Measure all qubits
    for i in range(8):
        machine << Measure(qubits[i], cbits[i])
    
    result = machine << qRunes()
    probs = result.get_probs()
    
    # Convert to binary string format
    dist = {}
    for outcome, prob in probs.items():
        # Convert integer outcome to 8-bit binary string
        binary_str = format(outcome, '08b')
        dist[binary_str] = prob
    
    return dist
