# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CPUQVM, H, CNOT

def collect_linear_blocks_with_and_without_limit():
    qvm = CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(5)

    linear_gates = [
        (H, [0]),
        (CNOT, [0, 1]),
        (CNOT, [1, 2]),
        (CNOT, [2, 3]),
        (CNOT, [3, 4]),
    ]

    def collect(max_block_width):
        blocks = []
        current_qubits = set()
        current_gates = []

        for gate_fn, qubit_indices in linear_gates:
            gate_qubits = set(qubit_indices)
            if current_gates and max_block_width is not None and len(current_qubits | gate_qubits) > max_block_width:
                blocks.append(current_gates)
                current_gates = []
                current_qubits = set()

            current_gates.append((gate_fn, qubit_indices))
            current_qubits |= gate_qubits

        if current_gates:
            blocks.append(current_gates)

        collected_circuit = QCircuit()
        for block_gates in blocks:
            block_circuit = QCircuit()
            for gate_fn, qubit_indices in block_gates:
                block_circuit << gate_fn(*[q[i] for i in qubit_indices])
            collected_circuit << block_circuit

        return collected_circuit

    full_block = collect(None)
    limited_block = collect(3)

    return full_block, limited_block
