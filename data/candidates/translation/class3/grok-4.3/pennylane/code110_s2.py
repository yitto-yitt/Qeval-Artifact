# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    def generate_random_clifford(num_qubits):
        with qml.tape.QuantumTape() as tape:
            num_gates = np.random.randint(10, 30)
            for _ in range(num_gates):
                gate_type = np.random.choice(['H', 'S', 'CNOT'])
                if gate_type == 'H':
                    wire = np.random.randint(num_qubits)
                    qml.Hadamard(wires=wire)
                elif gate_type == 'S':
                    wire = np.random.randint(num_qubits)
                    qml.S(wires=wire)
                elif gate_type == 'CNOT':
                    wires = np.random.choice(num_qubits, 2, replace=False)
                    qml.CNOT(wires=wires.tolist())
        return tape
    num_qubits = len(circuit.wires) if hasattr(circuit, 'wires') else getattr(circuit, 'num_qubits', 2)
    op_or = qml.matrix(circuit)
    qc_list = []
    counter = 0
    while counter < n:
        qc = generate_random_clifford(num_qubits)
        op_qc = qml.matrix(qc)
        if np.allclose(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
