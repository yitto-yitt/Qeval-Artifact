# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def collect_linear_blocks_with_and_without_limit():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]

    def collect(max_block_width=None):
        circuit = pq.QCircuit()
        circuit << pq.H(qubits[0])
        pending = []
        support = set()

        def append_block(block_edges):
            if len(block_edges) == 1:
                control, target = block_edges[0]
                circuit << pq.CNOT(qubits[control], qubits[target])
            elif block_edges:
                block = pq.QCircuit()
                for control, target in block_edges:
                    block << pq.CNOT(qubits[control], qubits[target])
                circuit << block

        for control, target in edges:
            expanded_support = support | {control, target}
            if (
                max_block_width is not None
                and len(expanded_support) > max_block_width
            ):
                append_block(pending)
                pending = []
                support = set()

            pending.append((control, target))
            support.update((control, target))

        append_block(pending)
        return circuit

    full_block = collect()
    limited_block = collect(max_block_width=3)

    for circuit in (full_block, limited_block):
        program = pq.QProg()
        program << circuit
        machine.prob_run_dict(program, qubits, -1)

    return full_block, limited_block


atexit.register(lambda: machine.finalize())
