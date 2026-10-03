# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def collect_linear_blocks_with_and_without_limit():
    def cnot_chain_unitary(num_wires, cnots):
        dim = 2 ** num_wires
        unitary = np.zeros((dim, dim), dtype=complex)
        for in_index in range(dim):
            bits = [(in_index >> (num_wires - 1 - i)) & 1 for i in range(num_wires)]
            for control, target in cnots:
                bits[target] ^= bits[control]
            out_index = 0
            for bit in bits:
                out_index = (out_index << 1) | bit
            unitary[out_index, in_index] = 1.0
        return unitary

    full_linear = cnot_chain_unitary(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    limited_linear = cnot_chain_unitary(3, [(0, 1), (1, 2)])

    full_block = qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(full_linear, wires=[0, 1, 2, 3, 4]),
        ]
    )

    limited_block = qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(limited_linear, wires=[0, 1, 2]),
            qml.QubitUnitary(limited_linear, wires=[2, 3, 4]),
        ]
    )

    return full_block, limited_block
