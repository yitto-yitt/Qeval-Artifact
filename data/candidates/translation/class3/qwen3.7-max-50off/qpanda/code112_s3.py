# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qc = QuantumCircuit(n_qubits)
    
    for pauli_string, time in zip(pauli_strings, times):
        dt = time / reps
        for _ in range(reps):
            # Basis change
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc.h(i)
                elif p == 'Y':
                    qc.h(i)
                    qc.s(i)
                    
            # CNOT cascade and Rz
            active_qubits = [i for i, p in enumerate(pauli_string) if p != 'I']
            if len(active_qubits) > 0:
                for i in range(len(active_qubits) - 1):
                    qc.cx(active_qubits[i], active_qubits[i+1])
                    
                qc.rz(2 * dt, active_qubits[-1])
                
                # Reverse CNOT cascade
                for i in range(len(active_qubits) - 2, -1, -1):
                    qc.cx(active_qubits[i], active_qubits[i+1])
                    
            # Inverse basis change
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    qc.h(i)
                elif p == 'Y':
                    qc.sdg(i)
                    qc.h(i)
                    
    return qc
