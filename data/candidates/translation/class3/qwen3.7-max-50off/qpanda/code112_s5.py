# EVAL_META: task_id=112, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, QCircuit, H, S, Sdg, CNOT, RZ

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    prog = QProg()
    qubits = prog.alloc_qubits(num_qubits)
    
    qc = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        t_step = time / reps if reps > 0 else 0.0
        for _ in range(reps):
            active_qubits = []
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc << H(qubits[i])
                    active_qubits.append(qubits[i])
                elif p == 'Y':
                    qc << Sdg(qubits[i])
                    qc << H(qubits[i])
                    active_qubits.append(qubits[i])
                elif p == 'Z':
                    active_qubits.append(qubits[i])
                    
            if len(active_qubits) > 0:
                for i in range(len(active_qubits) - 1):
                    qc << CNOT(active_qubits[i], active_qubits[i+1])
                    
                qc << RZ(active_qubits[-1], 2 * t_step)
                
                for i in range(len(active_qubits) - 2, -1, -1):
                    qc << CNOT(active_qubits[i], active_qubits[i+1])
                    
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc << H(qubits[i])
                elif p == 'Y':
                    qc << H(qubits[i])
                    qc << S(qubits[i])
                    
    prog << qc
    return prog
