# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def visualize_bell_states():
    machine = pq.QMachine()
    machine.init_qvm()
    
    # Prepare phi_plus state (|00> + |11>)
    qubits_phi_plus = machine.qAlloc_many(2)
    prog_phi_plus = pq.QProg()
    prog_phi_plus.insert(pq.H(qubits_phi_plus[0])).insert(pq.CNOT(qubits_phi_plus[0], qubits_phi_plus[1]))
    
    # Measure phi_plus
    cbits_phi_plus = machine.cAlloc_many(2)
    prog_phi_plus.insert(pq.Measure(qubits_phi_plus[0], cbits_phi_plus[0])).insert(pq.Measure(qubits_phi_plus[1], cbits_phi_plus[1]))
    
    # Run phi_plus circuit
    result_phi_plus = machine.run(prog_phi_plus, shots=1000)
    
    # Prepare phi_minus state (|00> - |11>)
    qubits_phi_minus = machine.qAlloc_many(2)
    prog_phi_minus = pq.QProg()
    prog_phi_minus.insert(pq.X(qubits_phi_minus[0])).insert(pq.H(qubits_phi_minus[0])).insert(pq.CNOT(qubits_phi_minus[0], qubits_phi_minus[1]))
    
    # Measure phi_minus
    cbits_phi_minus = machine.cAlloc_many(2)
    prog_phi_minus.insert(pq.Measure(qubits_phi_minus[0], cbits_phi_minus[0])).insert(pq.Measure(qubits_phi_minus[1], cbits_phi_minus[1]))
    
    # Run phi_minus circuit
    result_phi_minus = machine.run(prog_phi_minus, shots=1000)
    
    # Process results to get probability distributions
    def counts_to_probabilities(counts):
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    
    # Convert pyqpanda results to expected format
    phi_plus_counts = {}
    phi_minus_counts = {}
    
    # Extract counts from results
    for res in result_phi_plus:
        bits = ''.join(res)
        if bits in phi_plus_counts:
            phi_plus_counts[bits] += 1
        else:
            phi_plus_counts[bits] = 1
    
    for res in result_phi_minus:
        bits = ''.join(res)
        if bits in phi_minus_counts:
            phi_minus_counts[bits] += 1
        else:
            phi_minus_counts[bits] = 1
    
    # Convert to probabilities
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())
    
    phi_plus_probs = {key: value / phi_plus_total for key, value in phi_plus_counts.items()}
    phi_minus_probs = {key: value / phi_minus_total for key, value in phi_minus_counts.items()}
    
    machine.finalize()
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
