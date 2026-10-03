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

    full_block = build_circuit()
    limited_block = build_circuit()
    return full_block, limited_block


if __name__ == "__main__":
    full, limited = collect_linear_blocks_with_and_without_limit()
    print(full)
    print(limited)
    machine.finalize()
