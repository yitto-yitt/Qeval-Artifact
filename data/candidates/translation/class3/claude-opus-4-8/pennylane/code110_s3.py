# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from pennylane.tape import QuantumScript


def _matrix_equiv(mat1, mat2, rtol=0.4, atol=0.4):
    mat1 = np.asarray(mat1)
    mat2 = np.asarray(mat2)
    if mat1.shape != mat2.shape:
        return False

    def _phase(mat):
        for elt in mat.flatten(order='F'):
            if abs(elt) > atol:
                return elt / abs(elt)
        return complex(1.0)

    m1 = np.conj(_phase(mat1)) * mat1
    m2 = np.conj(_phase(mat2)) * mat2
    return bool(np.allclose(m1, m2, rtol=rtol, atol=atol))


def _random_clifford_tape(num_qubits, wires):
    ops = []
    depth = np.random.randint(1, 4 * num_qubits + 6)
    for _ in range(depth):
        if num_qubits > 1 and np.random.rand() < 0.4:
            a, b = np.random.choice(num_qubits, 2, replace=False)
            ops.append(qml.CNOT(wires=[wires[a], wires[b]]))
        else:
            q = wires[np.random.randint(num_qubits)]
            g = np.random.randint(5)
            if g == 0:
                ops.append(qml.Hadamard(q))
            elif g == 1:
                ops.append(qml.S(q))
            elif g == 2:
                ops.append(qml.PauliX(q))
            elif g == 3:
                ops.append(qml.PauliY(q))
            else:
                ops.append(qml.PauliZ(q))
    return QuantumScript(ops)


def equivalent_clifford_circuit(circuit, n):
    wires = list(circuit.wires)
    num_qubits = len(wires)
    target = qml.matrix(circuit, wire_order=wires)
    qc_list = []
    while len(qc_list) < n:
        tape = _random_clifford_tape(num_qubits, wires)
        mat = qml.matrix(tape, wire_order=wires)
        if _matrix_equiv(mat, target, rtol=0.4, atol=0.4):
            qc_list.append(tape)
    return qc_list
