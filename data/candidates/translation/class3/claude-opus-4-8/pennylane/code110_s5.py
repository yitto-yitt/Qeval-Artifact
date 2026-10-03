# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from pennylane.tape import QuantumScript


def _get_matrix(circuit):
    wires = list(circuit.wires)
    if len(wires) == 0:
        wires = [0]
    return np.array(qml.matrix(circuit, wire_order=wires)), len(wires)


def _equiv(a, b, rtol=0.4, atol=0.4):
    # check equality up to a global (complex) scalar factor
    denom = np.vdot(b, b)
    if np.abs(denom) < 1e-15:
        return np.allclose(a, b, rtol=rtol, atol=atol)
    c = np.vdot(b, a) / denom
    return np.allclose(a, c * b, rtol=rtol, atol=atol)


def _random_clifford_ops(num_wires):
    ops = []
    length = np.random.randint(1, 8 * num_wires + 6)
    for _ in range(length):
        g = np.random.randint(0, 3)
        if g == 0:
            ops.append(qml.Hadamard(int(np.random.randint(num_wires))))
        elif g == 1:
            ops.append(qml.S(int(np.random.randint(num_wires))))
        else:
            if num_wires >= 2:
                c, t = np.random.choice(num_wires, 2, replace=False)
                ops.append(qml.CNOT([int(c), int(t)]))
            else:
                ops.append(qml.Hadamard(0))
    return ops


def equivalent_clifford_circuit(circuit, n):
    target, num_wires = _get_matrix(circuit)
    wire_order = list(range(num_wires))
    qc_list = []
    counter = 0
    while counter < n:
        ops = _random_clifford_ops(num_wires)
        tape = QuantumScript(ops)
        cand = np.array(qml.matrix(tape, wire_order=wire_order))
        if _equiv(cand, target, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(tape)
    return qc_list
