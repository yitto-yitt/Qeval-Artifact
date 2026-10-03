# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT


def collect_linear_blocks_with_and_without_limit():
    circuits = []
    simulator = CPUQVM()

    for max_width in (5, 3):
        program = QProg()
        program << H(0)

        block = QCircuit()
        block_qubits = set()

        for control, target in ((0, 1), (1, 2), (2, 3), (3, 4)):
            gate_qubits = {control, target}
            if len(block_qubits | gate_qubits) > max_width:
                program << block
                block = QCircuit()
                block_qubits = set()

            block << CNOT(control, target)
            block_qubits.update(gate_qubits)

        if block_qubits:
            program << block

        simulator.run(program, 1)
        circuits.append(program)

    return tuple(circuits)
