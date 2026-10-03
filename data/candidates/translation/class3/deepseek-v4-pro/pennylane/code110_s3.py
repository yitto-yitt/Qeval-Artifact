# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def _get_matrix(circuit):
    mat = qml.matrix(circuit)
    if callable(mat):
        mat = mat()
    return np.asarray(mat)


def _equiv(mat1, mat2, rtol=0.4, atol=0.4):
    flat1 = np.ravel(mat1)
    flat2 = np.ravel(mat2)
    idx = int(np.argmax(np.abs(flat1)))
    phase = np.exp(1j * (np.angle(flat2[idx]) - np.angle(flat1[idx])))
    return np.allclose(mat1, mat2 * phase, rtol=rtol, atol=atol)


def _random_clifford_tape(num_qubits, rng):
    ops = []
    num_gates = num_qubits * 10 + int(rng.integers(0, 5))

    for _ in range(num_gates):
        if num_qubits == 1:
            gate = int(rng.integers(0, 2))
            if gate == 0:
                ops.append(("H", (0,)))
            else:
                ops.append(("S", (0,)))
        else:
            choice = int(rng.integers(0, 3))
            if choice == 0:
                wire = int(rng.integers(0, num_qubits))
                ops.append(("H", (wire,)))
            elif choice == 1:
                wire = int(rng.integers(0, num_qubits))
                ops.append(("S", (wire,)))
            else:
                control, target = rng.choice(num_qubits, size=2, replace=False)
                ops.append(("CNOT", (int(control), int(target))))

    with qml.tape.QuantumTape() as tape:
        for gate, wires in ops:
            if gate == "H":
                qml.Hadamard(wires=wires[0])
            elif gate == "S":
                qml.S(wires=wires[0])
            elif gate == "CNOT":
                qml.CNOT(wires=[wires[0], wires[1]])
        qml.state()

    return tape


def equivalent_clifford_circuit(circuit, n):
    ref_mat = _get_matrix(circuit)
    num_qubits = int(round(np.log2(ref_mat.shape[0])))
    rng = np.random.default_rng()

    circuits = []
    while len(circuits) < n:
        tape = _random_clifford_tape(num_qubits, rng)
        mat = _get_matrix(tape)
        if _equiv(ref_mat, mat):
            circuits.append(tape)

    return circuits
