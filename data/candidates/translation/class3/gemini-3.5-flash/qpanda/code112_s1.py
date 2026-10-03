# EVAL_META: task_id=112, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAllocMany(num_qubits)
    
    circuit = pq.QCircuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        # Find active qubits
        active_qubits = []
        for i in range(num_qubits):
            op = pauli_string[num_qubits - 1 - i]
            if op != 'I':
                active_qubits.append(i)
                
        if not active_qubits:
            continue
            
        for _ in range(reps):
            # Basis change before
            for q_idx in active_qubits:
                op = pauli_string[num_qubits - 1 - q_idx]
                if op == 'X':
                    circuit << pq.H(q[q_idx])
                elif op == 'Y':
                    circuit << pq.RX(q[q_idx], np.pi / 2)
            
            # CNOT ladder
            for j in range(len(active_qubits) - 1):
                circuit << pq.CNOT(q[active_qubits[j]], q[active_qubits[j+1]])
                
            # RZ rotation
            last_q = active_qubits[-1]
            circuit << pq.RZ(q[last_q], 2 * time / reps)
            
            # CNOT ladder reverse
            for j in range(len(active_qubits) - 2, -1, -1):
                circuit << pq.CNOT(q[active_qubits[j]], q[active_qubits[j+1]])
                
            # Basis change after
            for q_idx in active_qubits:
                op = pauli_string[num_qubits - 1 - q_idx]
                if op == 'X':
                    circuit << pq.H(q[q_idx])
                elif op == 'Y':
                    circuit << pq.RX(q[q_idx], -np.pi / 2)
                    
    return circuit
