# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    # Create quantum machine and allocate qubits
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(len(pauli_string))
    
    # Build the Hamiltonian based on Pauli string
    hamiltonian = []
    for i, pauli_op in enumerate(pauli_string):
        if pauli_op == 'X':
            hamiltonian.append([1.0, f"X {i}"])
        elif pauli_op == 'Y':
            hamiltonian.append([1.0, f"Y {i}"])
        elif pauli_op == 'Z':
            hamiltonian.append([1.0, f"Z {i}"])
        # 'I' is ignored as it doesn't contribute to evolution
    
    # Create the evolution circuit
    prog = QProg()
    
    # Apply evolution based on the Hamiltonian terms
    for coeff, term in hamiltonian:
        if term.startswith('X'):
            idx = int(term.split()[1])
            prog << RX(qubits[idx], -2 * coeff * time)
        elif term.startswith('Y'):
            idx = int(term.split()[1])
            prog << RY(qubits[idx], -2 * coeff * time)
        elif term.startswith('Z'):
            idx = int(term.split()[1])
            prog << RZ(qubits[idx], -2 * coeff * time)
    
    # Convert to circuit
    circuit = QCircuit()
    circuit << prog
    
    return circuit
