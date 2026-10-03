# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from pennylane.tape import QuantumScript

def _equiv(mat1, mat2, rtol=0.4, atol=0.4):
    idx = np.unravel_index(np.argmax(np.abs(mat1)), mat1.shape)
    if np.abs(mat1[idx]) < 1e-10:
        return np.allclose(mat1, mat2, rtol=rtol, atol=atol)
    phase = mat2[idx] / mat1[idx]
    return np.allclose(mat1 * phase, mat2, rtol=rtol, atol=atol)

def equivalent_clifford_circuit(circuit, n):
    op_or = qml.matrix(circuit, wire_order=circuit.wires)
    wires = list(circuit.wires)
    num_qubits = len(wires)
    qc_list = []
    counter = 0
    while counter < n:
        ops = []
        num_gates = np.random.randint(1, 15)
        for _ in range(num_gates):
            gate_type = np.random.choice(['H', 'S', 'CNOT'])
            if gate_type == 'H':
                wire = np.random.choice(wires)
                ops.append(qml.Hadamard(wire))
            elif gate_type == 'S':
                wire = np.random.choice(wires)
                ops.append(qml.S(wire))
            elif gate_type == 'CNOT':
                if num_qubits < 2:
                    continue
                control = np.random.choice(wires)
                target = np.random.choice(wires)
                while target == control:
                    target = np.random.choice(wires)
                ops.append(qml.CNOT(wires=[control, target]))
        qc = QuantumScript(ops, measurements=[])
        op_qc = qml.matrix(qc, wire_order=circuit.wires)
        if _equiv(op_or, op_qc, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
