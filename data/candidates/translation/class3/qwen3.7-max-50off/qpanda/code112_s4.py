# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3 import QuantumCircuit, H, CNOT, RX, RZ
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qc = QuantumCircuit(n_qubits)
    qubits = qc.qubits
    
    for pauli_string, t in zip(pauli_strings, times):
        active_qubits = [i for i, p in enumerate(pauli_string) if p != 'I']
        
        for _ in range(int(reps)):
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc << H(qubits[i])
                elif p == 'Y':
                    qc << RX(qubits[i], np.pi/2)
                    
            for j in range(len(active_qubits) - 1):
                qc << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j+1]])
                
            if len(active_qubits) > 0:
                qc << RZ(qubits[active_qubits[-1]], 2 * t / reps)
                
            for j in range(len(active_qubits) - 2, -1, -1):
                qc << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j+1]])
                
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc << H(qubits[i])
                elif p == 'Y':
                    qc << RX(qubits[i], -np.pi/2)
                    
    return qc
