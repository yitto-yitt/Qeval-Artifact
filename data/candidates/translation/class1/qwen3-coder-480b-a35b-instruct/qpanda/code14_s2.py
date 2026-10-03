# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
from pyqpanda3.algorithms import *
from pyqpanda3.machine import *

def bell_each_shot():
    # Create quantum program
    prog = QProg()
    
    # Allocate qubits and classical bits
    qubits = pq.qAlloc_many(2)
    cbits = pq.cAlloc_many(2)
    
    # Apply gates: H on first qubit, then CNOT
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    # Measure all qubits
    prog << pq.Measure(qubits[0], cbits[0]) << pq.Measure(qubits[1], cbits[1])
    
    # Initialize quantum machine
    machine = pq.QMachine()
    machine.init()
    
    # Run the program 10 times (shots)
    results = []
    for _ in range(10):
        result = machine.run(prog)
        # Extract measurement results
        bitstring = ""
        for i in range(2):
            bitstring += str(result[cbits[i]])
        results.append(bitstring)
        # Reset for next shot
        machine.reset()
    
    machine.finalize()
    
    # Count occurrences of each bitstring
    counts = {}
    for bitstring in results:
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert to probabilities
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
