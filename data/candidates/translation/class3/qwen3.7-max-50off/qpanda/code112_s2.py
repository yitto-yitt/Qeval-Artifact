# EVAL_META: task_id=112, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, RX, RZ, CNOT

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qc = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        theta = time / reps
        for _ in range(reps):
            n = len(pauli_string)
            active_qubits = []
            
            for i in range(n):
                p = pauli_string[n - 1 - i]
                if p == 'X':
                    qc << H(i)
                    active_qubits.append(i)
                elif p == 'Y':
                    qc << RX(i, np.pi/2)
                    active_qubits.append(i)
                elif p == 'Z':
                    active_qubits.append(i)
                    
            if not active_qubits:
                continue
                
            for i in range(len(active_qubits) - 1):
                qc << CNOT(active_qubits[i], active_qubits[i+1])
                
            qc << RZ(active_qubits[-1], 2 * theta)
            
            for i in range(len(active_qubits) - 2, -1, -1):
                qc << CNOT(active_qubits[i], active_qubits[i+1])
                
            for i in range(n):
                p = pauli_string[n - 1 - i]
                if p == 'X':
                    qc << H(i)
                elif p == 'Y':
                    qc << RX(i, -np.pi/2)
                    
    return qc
