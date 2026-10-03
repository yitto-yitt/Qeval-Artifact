# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    qc = cirq.Circuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            t = time / reps
            circ = cirq.Circuit()
            active_qubits = []
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    circ.append(cirq.H(qubits[i]))
                    active_qubits.append(qubits[i])
                elif p == 'Y':
                    circ.append((cirq.S**-1).on(qubits[i]))
                    circ.append(cirq.H(qubits[i]))
                    active_qubits.append(qubits[i])
                elif p == 'Z':
                    active_qubits.append(qubits[i])
            
            if len(active_qubits) > 0:
                for i in range(len(active_qubits) - 1):
                    circ.append(cirq.CNOT(active_qubits[i], active_qubits[i+1]))
                
                circ.append(cirq.Rz(rads=2 * t).on(active_qubits[-1]))
                
                for i in range(len(active_qubits) - 2, -1, -1):
                    circ.append(cirq.CNOT(active_qubits[i], active_qubits[i+1]))
                    
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    circ.append(cirq.H(qubits[i]))
                elif p == 'Y':
                    circ.append(cirq.H(qubits[i]))
                    circ.append(cirq.S(qubits[i]))
                    
            qc.append(circ)
            
    return qc
