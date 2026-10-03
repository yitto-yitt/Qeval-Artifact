# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def _linear_block_matrix(cx_pairs, wires):
    ops = [qml.CNOT(wires=list(p)) for p in cx_pairs]
    tape = qml.tape.QuantumScript(ops)
    return qml.matrix(tape, wire_order=wires)


def collect_linear_blocks_with_and_without_limit():
    # Original circuit: H(0) followed by a chain of CX gates on 5 qubits.
    # The H gate is non-linear (in the Clifford-linear sense) and separates
    # it from the collectible linear (CX) block.

    # ---- No block width restriction ----
    # All 4 CX gates collapse into a single linear function over qubits 0-4.
    full_wires = [0, 1, 2, 3, 4]
    U_full = _linear_block_matrix([(0, 1), (1, 2), (2, 3), (3, 4)], full_wires)
    full_ops = [
        qml.Hadamard(wires=0),
        qml.QubitUnitary(U_full, wires=full_wires),
    ]
    full_block = qml.tape.QuantumScript(full_ops)

    # ---- max_block_width = 3 ----
    # cx(0,1),cx(1,2) span qubits {0,1,2} (width 3); adding cx(2,3) would
    # exceed width 3, so a new block is started with cx(2,3),cx(3,4).
    U_block1 = _linear_block_matrix([(0, 1), (1, 2)], [0, 1, 2])
    U_block2 = _linear_block_matrix([(2, 3), (3, 4)], [2, 3, 4])
    limited_ops = [
        qml.Hadamard(wires=0),
        qml.QubitUnitary(U_block1, wires=[0, 1, 2]),
        qml.QubitUnitary(U_block2, wires=[2, 3, 4]),
    ]
    limited_block = qml.tape.QuantumScript(limited_ops)

    return full_block, limited_block
