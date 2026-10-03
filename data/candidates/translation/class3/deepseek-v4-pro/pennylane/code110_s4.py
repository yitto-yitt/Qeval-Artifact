# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import random

def _random_identity_ops(wires, num_qubits):
    ops = []
    for _ in range(random.randint(1, 4)):
        gate = random.choice(["H", "S", "X", "CNOT"])
        if gate == "H":
            w = random.choice(wires)
            ops.append(qml.Hadamard(wires=w))
            ops.append(qml.Hadamard(wires=w))
        elif gate == "S":
            w = random.choice(wires)
            for _ in range(4):
                ops.append(qml.S(wires=w))
        elif gate == "X":
            w = random.choice(wires)
            ops.append(qml.PauliX(wires=w))
            ops.append(qml.PauliX(wires=w))
        elif gate == "CNOT" and num_qubits >= 2:
            c, t = random.sample(wires, 2)
            ops.append(qml.CNOT(wires=[c, t]))
            ops.append(qml.CNOT(wires=[c, t]))
    return ops

def equivalent_clifford_circuit(circuit, n):
    wires = list(circuit.wires)
    original_ops = list(circuit.operations)
    num_qubits = len(wires)
    qc_list = []
    for _ in range(n):
        ops = original_ops + _random_identity_ops(wires, num_qubits)
        qc_list.append(qml.tape.QuantumTape(ops, []))
    return qc_list
