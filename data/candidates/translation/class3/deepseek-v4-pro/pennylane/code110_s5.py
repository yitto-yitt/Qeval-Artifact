# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def _random_identity_block(wires, rng):
    wires = list(wires)
    num_wires = len(wires)
    ops = []

    for _ in range(int(rng.integers(1, 5))):
        if num_wires > 1 and rng.random() < 0.3:
            idx = rng.choice(num_wires, size=2, replace=False).tolist()
            w0, w1 = wires[int(idx[0])], wires[int(idx[1])]
            op = qml.CNOT(wires=[w0, w1])
            inv = qml.adjoint(qml.CNOT(wires=[w0, w1]))
        else:
            wire = wires[int(rng.integers(0, num_wires))]
            gate = int(rng.integers(0, 4))

            if gate == 0:
                op = qml.Hadamard(wires=wire)
                inv = qml.adjoint(qml.Hadamard(wires=wire))
            elif gate == 1:
                op = qml.S(wires=wire)
                inv = qml.adjoint(qml.S(wires=wire))
            elif gate == 2:
                op = qml.PauliX(wires=wire)
                inv = qml.adjoint(qml.PauliX(wires=wire))
            else:
                op = qml.PauliZ(wires=wire)
                inv = qml.adjoint(qml.PauliZ(wires=wire))

        ops.extend([op, inv])

    return ops

def equivalent_clifford_circuit(circuit, n):
    if hasattr(circuit, "operations"):
        base_ops = list(circuit.operations)
        wires = circuit.wires
    elif hasattr(circuit, "qtape"):
        base_ops = list(circuit.qtape.operations)
        wires = circuit.qtape.wires
    else:
        base_ops = []
        wires = None

    if wires is None or len(wires) == 0:
        mat = qml.matrix(circuit)
        num_qubits = int(round(np.log2(mat.shape[0])))
        wires = list(range(num_qubits))

    rng = np.random.default_rng()
    qc_list = []

    for _ in range(n):
        qc_list.append(qml.tape.QuantumScript(base_ops + _random_identity_block(wires, rng)))

    return qc_list
