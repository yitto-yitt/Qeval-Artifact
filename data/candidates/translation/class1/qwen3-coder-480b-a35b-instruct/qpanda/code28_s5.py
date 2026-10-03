# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def visualize_bell_states():
    # Prepare phi_plus circuit
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog_plus = pq.QProg()
    prog_plus << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog_plus << MEASURE(qubits[0], cbits[0]) << MEASURE(qubits[1], cbits[1])
    
    result_plus = machine.run(prog_plus, shots=1000)
    counts_plus = result_plus.get_q_result()
    
    # Reset machine for phi_minus
    machine.finalize()
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog_minus = pq.QProg()
    prog_minus << X(qubits[0]) << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog_minus << MEASURE(qubits[0], cbits[0]) << MEASURE(qubits[1], cbits[1])
    
    result_minus = machine.run(prog_minus, shots=1000)
    counts_minus = result_minus.get_q_result()
    
    # Convert to probability distributions
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    phi_plus_probs = {key: value / total_plus for key, value in counts_plus.items()}
    phi_minus_probs = {key: value / total_minus for key, value in counts_minus.items()}
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
