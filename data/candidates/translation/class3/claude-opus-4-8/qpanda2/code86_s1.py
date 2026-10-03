# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def collect_linear_blocks_with_and_without_limit():
    def build_circuit():
        circ = QCircuit()
        circ << H(qubits[0])
        circ << CNOT(qubits[0], qubits[1])
        circ << CNOT(qubits[1], qubits[2])
        circ << CNOT(qubits[2], qubits[3])
        circ << CNOT(qubits[3], qubits[4])
        return circ

    def collect_linear(gates, max_block_width=None):
        blocks = []
        current = []
        current_qubits = set()

        def is_linear(name):
            return name in ("CNOT", "CX")

        for g in gates:
            name, involved = g
            if is_linear(name):
                new_qubits = current_qubits | set(involved)
                if max_block_width is not None and len(new_qubits) > max_block_width:
                    if current:
                        blocks.append((list(current), set(current_qubits)))
                    current = [g]
                    current_qubits = set(involved)
                else:
                    current.append(g)
                    current_qubits = new_qubits
            else:
                if current:
                    blocks.append((list(current), set(current_qubits)))
                    current = []
                    current_qubits = set()
                blocks.append(([g], set(involved)))
        if current:
            blocks.append((list(current), set(current_qubits)))
        return blocks

    gate_list = [
        ("H", [0]),
        ("CNOT", [0, 1]),
        ("CNOT", [1, 2]),
        ("CNOT", [2, 3]),
        ("CNOT", [3, 4]),
    ]

    full_blocks = collect_linear(gate_list, max_block_width=None)
    limited_blocks = collect_linear(gate_list, max_block_width=3)

    full_circuit = build_circuit()
    limited_circuit = build_circuit()

    machine.finalize()

    return (full_circuit, full_blocks), (limited_circuit, limited_blocks)


if __name__ == "__main__":
    result = collect_linear_blocks_with_and_without_limit()
    print(result)
