# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def collect_linear_blocks_with_and_without_limit():
    circuits = []

    for max_block_width in (None, 3):
        circuit = pq.QCircuit()
        circuit << pq.H(qubits[0])

        block = pq.QCircuit()
        block_qubits = set()

        for control, target in ((0, 1), (1, 2), (2, 3), (3, 4)):
            gate_qubits = {control, target}
            if (
                max_block_width is not None
                and len(block_qubits | gate_qubits) > max_block_width
            ):
                circuit << block
                block = pq.QCircuit()
                block_qubits = set()

            block << pq.CNOT(qubits[control], qubits[target])
            block_qubits.update(gate_qubit for gate_qubit in gate_qubits)

        if block_qubits:
            circuit << block

        program = pq.QProg()
        for qubit in qubits:
            program << pq.Reset(qubit)
        program << circuit
        machine.directly_run(program)
        circuits.append(circuit)

    return tuple(circuits)


atexit.register(machine.finalize)
