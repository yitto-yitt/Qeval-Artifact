# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def collect_linear_blocks_with_and_without_limit():
    edges = ((0, 1), (1, 2), (2, 3), (3, 4))
    circuits = []

    for max_block_width in (None, 3):
        circuit = pq.QCircuit()
        circuit << pq.H(qubits[0])

        block = pq.QCircuit()
        block_qubits = set()

        for control, target in edges:
            expanded_qubits = block_qubits | {control, target}

            if (
                max_block_width is not None
                and len(expanded_qubits) > max_block_width
            ):
                circuit << block
                block = pq.QCircuit()
                block_qubits = set()

            block << pq.CNOT(qubits[control], qubits[target])
            block_qubits.update((control, target))

        if block_qubits:
            circuit << block

        program = pq.QProg()
        program << circuit
        machine.directly_run(program)
        circuits.append(circuit)

    return circuits[0], circuits[1]


atexit.register(machine.finalize)
