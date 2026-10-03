# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    for pauli_str, time in zip(pauli_strings, times):
        for _ in range(reps):
            t_step = time / reps
            ops = []
            active_qubits = []
            for q, p in zip(qubits, pauli_str):
                if p == 'I':
                    continue
                active_qubits.append(q)
                if p == 'X':
                    ops.append(cirq.H(q))
                elif p == 'Y':
                    ops.append(cirq.S(q))
                    ops.append(cirq.H(q))
            
            if len(active_qubits) > 0:
                for i in range(len(active_qubits) - 1):
                    ops.append(cirq.CNOT(active_qubits[i], active_qubits[i+1]))
                
                ops.append(cirq.rz(2 * t_step)(active_qubits[-1]))
                
                for i in range(len(active_qubits) - 2, -1, -1):
                    ops.append(cirq.CNOT(active_qubits[i], active_qubits[i+1]))
                    
            for q, p in zip(qubits, pauli_str):
                if p == 'X':
                    ops.append(cirq.H(q))
                elif p == 'Y':
                    ops.append(cirq.H(q))
                    ops.append(cirq.S(q)**-1)
                    
            circuit.append(ops)
            
    return circuit
