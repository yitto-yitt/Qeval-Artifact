# EVAL_META: task_id=50, framework=qpanda2, class=3
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def remove_gate_in_position(circuit, position):
    position = operator.index(position)
    nodes = []
    iterator = circuit.get_first_node_iter()
    end = circuit.get_end_node_iter()

    while iterator != end:
        nodes.append(iterator)
        iterator = iterator.get_next()

    circuit.delete_qnode(nodes[position])
    return circuit


machine.finalize()
