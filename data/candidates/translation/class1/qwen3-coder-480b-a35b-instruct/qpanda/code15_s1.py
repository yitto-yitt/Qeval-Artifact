# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda import *
import numpy as np

def noisy_bell():
    # Initialize QPanda environment
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Create quantum machine and allocate qubits/cbits
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    # Build the Bell circuit
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(Measure(qubits[0], cbits[0]))
    prog.insert(Measure(qubits[1], cbits[1]))
    
    # Run the circuit
    result = qvm.run_with_configuration(prog, cbits, 1000)
    
    # Normalize the results to get probabilities
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
