# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
from pyqpanda3.algorithms import QMachine
import math

def and_gate(a, b):
    machine = QMachine()
    machine.init_qvm()
    
    # Allocate qubits
    qubits = machine.qAlloc_many(9)  # 3 for a + 3 for b + 3 ancillary
    cbits = machine.cAlloc_many(3)   # 3 classical bits for measurement
    
    # Separate qubits
    qr_a = qubits[:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    
    # Initialize input values
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '1':
            machine << pq.X(qr_a[i])
        if b_str[2-i] == '1':
            machine << pq.X(qr_b[i])
    
    # Apply CCX (Toffoli) gates for AND operation
    for i in range(3):
        machine << pq.CCX(qr_a[i], qr_b[i], ancillary[i])
    
    # Measure ancillary qubits
    for i in range(3):
        machine << pq.Measure(ancillary[i], cbits[i])
    
    # Run the program
    result = machine.run_and_get_result()
    
    # Extract counts and normalize to probabilities
    counts = {}
    for key, value in result.items():
        # Convert the result string to just the measured bits (last 3 bits)
        # Since we only measure the last 3 qubits, the result should directly be 3-bit string
        counts[key] = float(value)
    
    total = sum(counts.values())
    probabilities = {key: value / total for key, value in counts.items()}
    
    machine.finalize()
    return probabilities
