# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *
from pyqpanda3.utils import *

def xor_gate(a, b):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    # Convert integers to binary representation
    a_bits = [int(bit) for bit in format(a, '08b')]
    b_bits = [int(bit) for bit in format(b, '08b')]
    
    # Apply X gates based on bits of a
    for i, bit in enumerate(reversed(a_bits)):
        if bit == 1:
            machine << X(qubits[i])
    
    # Apply XOR operation (CNOT gates) with b as control
    for i, bit in enumerate(reversed(b_bits)):
        if bit == 1:
            machine << X(qubits[i])
    
    # Measure all qubits
    for i in range(8):
        machine << Measure(qubits[i], cbits[i])
    
    result = machine.run()
    
    # Count results
    counts = {}
    for res_str, count in result.items():
        # Reverse the bit string to match expected order
        reversed_str = res_str[::-1]
        counts[reversed_str] = count
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
