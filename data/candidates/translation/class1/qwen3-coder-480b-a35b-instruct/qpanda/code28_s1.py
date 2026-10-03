# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda import *
import numpy as np

def visualize_bell_states():
    # Initialize QPanda
    machine = init(QMachineType.CPU)
    
    # Create phi_plus circuit
    prog_phi_plus = QProg()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog_phi_plus.insert(H(qubits[0]))
    prog_phi_plus.insert(CNOT(qubits[0], qubits[1]))
    prog_phi_plus.insert(Measure(qubits[0], cbits[0]))
    prog_phi_plus.insert(Measure(qubits[1], cbits[1]))
    
    # Create phi_minus circuit
    prog_phi_minus = QProg()
    qubits2 = machine.qAlloc_many(2)
    cbits2 = machine.cAlloc_many(2)
    
    prog_phi_minus.insert(X(qubits2[0]))
    prog_phi_minus.insert(H(qubits2[0]))
    prog_phi_minus.insert(CNOT(qubits2[0], qubits2[1]))
    prog_phi_minus.insert(Measure(qubits2[0], cbits2[0]))
    prog_phi_minus.insert(Measure(qubits2[1], cbits2[1]))
    
    # Run simulations
    machine.set_configure(1000, 1000)  # shots=1000
    machine.run(prog_phi_plus)
    phi_plus_result = machine.get_measure_counts()
    
    machine.run(prog_phi_minus)
    phi_minus_result = machine.get_measure_counts()
    
    # Normalize counts to probabilities
    phi_plus_total = sum(phi_plus_result.values())
    phi_minus_total = sum(phi_minus_result.values())
    
    phi_plus_probs = {key: value / phi_plus_total for key, value in phi_plus_result.items()}
    phi_minus_probs = {key: value / phi_minus_total for key, value in phi_minus_result.items()}
    
    # Clean up
    finalize()
    
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
