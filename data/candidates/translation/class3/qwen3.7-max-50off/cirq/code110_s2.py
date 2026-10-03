# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    num_qubits = len(qubits)
    result = []
    
    clifford_gates_1q = [cirq.X, cirq.Y, cirq.Z, cirq.H]
    
    for _ in range(n):
        new_circuit = cirq.Circuit(circuit)
        num_identities = np.random.randint(1, 5)
        for _ in range(num_identities):
            if num_qubits > 0:
                q = qubits[np.random.randint(num_qubits)]
                g = clifford_gates_1q[np.random.randint(len(clifford_gates_1q))]
                new_circuit.append(g(q))
                new_circuit.append(g(q))
            if num_qubits > 1 and np.random.random() > 0.5:
                q1, q2 = np.random.choice(qubits, 2, replace=False)
                new_circuit.append(cirq.CNOT(q1, q2))
                new_circuit.append(cirq.CNOT(q1, q2))
        result.append(new_circuit)
        
    return result
