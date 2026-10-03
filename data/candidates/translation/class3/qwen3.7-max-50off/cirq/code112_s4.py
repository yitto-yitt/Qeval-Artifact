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
            for p, q in zip(pauli_str, qubits):
                if p == 'X':
                    ops.append(cirq.H(q))
                    active_qubits.append(q)
                elif p == 'Y':
                    ops.append(cirq.rx(np.pi/2)(q))
                    active_qubits.append(q)
                elif p == 'Z':
                    active_qubits.append(q)
                elif p == 'I':
                    pass
            
            if active_qubits:
                for i in range(len(active_qubits) - 1):
                    ops.append(cirq.CNOT(active_qubits[i], active_qubits[i+1]))
                    
                ops.append(cirq.rz(2 * t_step)(active_qubits[-1]))
                
                for i in range(len(active_qubits) - 2, -1, -1):
                    ops.append(cirq.CNOT(active_qubits[i], active_qubits[i+1]))
                    
                for p, q in zip(pauli_str, qubits):
                    if p == 'X':
                        ops.append(cirq.H(q))
                    elif p == 'Y':
                        ops.append(cirq.rx(-np.pi/2)(q))
            else:
                ops.append(cirq.GlobalPhaseGate(np.exp(-1j * t_step)).on())
                
            circuit.append(ops)
            
    return circuit
