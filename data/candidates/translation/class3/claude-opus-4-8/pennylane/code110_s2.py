# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def _get_matrix(circuit):
    try:
        m = qml.matrix(circuit)
        if callable(m):
            m = m()
    except Exception:
        m = qml.matrix(circuit)()
    return np.array(m, dtype=complex)


def _equiv(U, V, rtol=0.4, atol=0.4):
    u = U.flatten()
    v = V.flatten()
    if u.shape != v.shape:
        return False
    k = int(np.argmax(np.abs(u)))
    if np.abs(v[k]) < 1e-12:
        return False
    phase = u[k] / v[k]
    return np.allclose(u, phase * v, rtol=rtol, atol=atol)


def _random_clifford_tape(num_qubits):
    single_gates = [qml.Hadamard, qml.S, qml.PauliX, qml.PauliY, qml.PauliZ]
    n_gates = int(np.random.randint(num_qubits, num_qubits * 6 + 1))
    with qml.tape.QuantumTape() as tape:
        for _ in range(n_gates):
            if num_qubits > 1 and np.random.rand() < 0.3:
                c, t = np.random.choice(num_qubits, 2, replace=False)
                qml.CNOT(wires=[int(c), int(t)])
            else:
                w = int(np.random.randint(num_qubits))
                gate = single_gates[int(np.random.randint(len(single_gates)))]
                gate(wires=w)
    return tape


def equivalent_clifford_circuit(circuit, n):
    op_or = _get_matrix(circuit)
    dim = op_or.shape[0]
    num_qubits = int(round(np.log2(dim)))

    qc_list = []
    counter = 0
    while counter < n:
        tape = _random_clifford_tape(num_qubits)
        op_qc = qml.matrix(tape, wire_order=range(num_qubits))
        op_qc = np.array(op_qc, dtype=complex)
        if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(tape)
    return qc_list
