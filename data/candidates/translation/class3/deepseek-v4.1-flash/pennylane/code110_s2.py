# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np
import random
from pennylane.workflow import construct_tape

def equivalent_clifford_circuit(circuit, n):
    # Extract the operations and wires from the given circuit
    if isinstance(circuit, qml.QNode):
        if hasattr(circuit, 'tape') and circuit.tape is not None:
            tape = circuit.tape
        elif hasattr(circuit, 'qtape') and circuit.qtape is not None:
            tape = circuit.qtape
        else:
            tape = construct_tape(circuit)()
        original_ops = tape.operations
        wire_list = list(tape.wires)
    elif callable(circuit):
        with qml.tape.QuantumTape() as tape:
            circuit()
        original_ops = tape.operations
        wire_list = list(tape.wires)
    elif hasattr(circuit, 'operations'):
        original_ops = circuit.operations
        wire_list = list(circuit.wires)
    else:
        raise ValueError("Unsupported circuit type")

    # Fallback if no wires are found (e.g., empty circuit)
    if len(wire_list) == 0:
        mat_orig = qml.matrix(circuit)()
        num_qubits = int(np.log2(mat_orig.shape[0]))
        wire_list = list(range(num_qubits))

    def random_clifford_ops(wires, depth=20):
        """Generate a random sequence of self-inverse Clifford gates."""
        ops = []
        gates = ['H', 'X', 'Y', 'Z', 'CNOT', 'SWAP']
        for _ in range(depth):
            gate = random.choice(gates)
            if gate == 'H':
                i = random.choice(wires)
                ops.append(qml.Hadamard(wires=i))
            elif gate == 'X':
                i = random.choice(wires)
                ops.append(qml.PauliX(wires=i))
            elif gate == 'Y':
                i = random.choice(wires)
                ops.append(qml.PauliY(wires=i))
            elif gate == 'Z':
                i = random.choice(wires)
                ops.append(qml.PauliZ(wires=i))
            elif gate == 'CNOT':
                if len(wires) < 2:
                    continue
                i, j = random.sample(wires, 2)
                ops.append(qml.CNOT(wires=[i, j]))
            elif gate == 'SWAP':
                if len(wires) < 2:
                    continue
                i, j = random.sample(wires, 2)
                ops.append(qml.SWAP(wires=[i, j]))
        return ops

    qc_list = []
    for _ in range(n):
        # Random self-inverse Clifford circuit
        R = random_clifford_ops(wire_list, depth=20)
        # Identity circuit: R followed by its reverse (since all gates are self-inverse)
        identity_ops = R + R[::-1]
        # Combine with original operations
        full_ops = original_ops + identity_ops
        qs = qml.tape.QuantumScript(full_ops, [])
        qc_list.append(qs)
    return qc_list
