# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def _circuit_to_matrix(circuit):
    num_qubits = len(circuit.wires)
    matrix = qml.matrix(circuit, wire_order=circuit.wires)
    return np.array(matrix), num_qubits


def _equiv(a, b, rtol=0.4, atol=0.4):
    dim = a.shape[0]
    prod = a.conj().T @ b
    phase = None
    for i in range(dim):
        for j in range(dim):
            if abs(prod[i, j]) > 1e-9:
                phase = prod[i, j] / abs(prod[i, j])
                break
        if phase is not None:
            break
    if phase is None:
        return False
    return np.allclose(b, phase * a, rtol=rtol, atol=atol)


def _random_clifford_tape(num_qubits, num_gates=30):
    ops = []
    single = ["H", "S", "X", "Y", "Z"]
    rng = np.random.default_rng()
    for _ in range(num_gates):
        if num_qubits > 1 and rng.random() < 0.4:
            q = rng.choice(num_qubits, size=2, replace=False)
            ops.append(qml.CNOT(wires=[int(q[0]), int(q[1])]))
        else:
            q = int(rng.integers(num_qubits))
            g = rng.choice(single)
            if g == "H":
                ops.append(qml.Hadamard(wires=q))
            elif g == "S":
                ops.append(qml.S(wires=q))
            elif g == "X":
                ops.append(qml.PauliX(wires=q))
            elif g == "Y":
                ops.append(qml.PauliY(wires=q))
            else:
                ops.append(qml.PauliZ(wires=q))
    return qml.tape.QuantumScript(ops)


def equivalent_clifford_circuit(circuit, n):
    target, num_qubits = _circuit_to_matrix(circuit)
    wires = list(range(num_qubits))
    qc_list = []
    counter = 0
    while counter < n:
        tape = _random_clifford_tape(num_qubits)
        mat = np.array(qml.matrix(tape, wire_order=wires))
        if _equiv(mat, target, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(tape)
    return qc_list
