# EVAL_META: task_id=112, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumCircuit, H, CNOT, RZ

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qc = QuantumCircuit(num_qubits)
    
    for pauli_string, time in zip(pauli_strings, times):
        dt = time / reps
        for _ in range(int(reps)):
            # Basis change
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc << H(i)
                elif p == 'Y':
                    qc << RZ(-np.pi/2, i)
                    qc << H(i)
                    
            # CNOT cascade
            active_qubits = [i for i, p in enumerate(pauli_string) if p != 'I']
            if len(active_qubits) > 0:
                for i in range(len(active_qubits) - 1):
                    qc << CNOT(active_qubits[i], active_qubits[i+1])
                    
                # Rz rotation
                qc << RZ(2 * dt, active_qubits[-1])
                
                # Reverse CNOT cascade
                for i in range(len(active_qubits) - 2, -1, -1):
                    qc << CNOT(active_qubits[i], active_qubits[i+1])
                    
            # Inverse basis change
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc << H(i)
                elif p == 'Y':
                    qc << H(i)
                    qc << RZ(np.pi/2, i)
                    
    return qc
