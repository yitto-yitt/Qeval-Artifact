# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    qc_list = []
    qubits = sorted(list(circuit.all_qubits()))
    if not qubits:
        qubits = [cirq.LineQubit(0)]
        
    for _ in range(n):
        new_circuit = circuit.copy()
        num_insertions = np.random.randint(1, 6)
        for _ in range(num_insertions):
            q = np.random.choice(qubits)
            gate_type = np.random.randint(0, 5)
            if gate_type == 0:
                new_circuit.append(cirq.X(q))
                new_circuit.append(cirq.X(q))
            elif gate_type == 1:
                new_circuit.append(cirq.Y(q))
                new_circuit.append(cirq.Y(q))
            elif gate_type == 2:
                new_circuit.append(cirq.Z(q))
                new_circuit.append(cirq.Z(q))
            elif gate_type == 3:
                new_circuit.append(cirq.H(q))
                new_circuit.append(cirq.H(q))
            elif gate_type == 4:
                new_circuit.append(cirq.S(q))
                new_circuit.append(cirq.Z(q))
                new_circuit.append(cirq.S(q))
        qc_list.append(new_circuit)
        
    return qc_list
