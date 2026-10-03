# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def remove_gate_in_position(circuit, position):
    nodes = []
    iterator = circuit.get_first_node_iter()
    end = circuit.get_end_node_iter()

    while iterator != end:
        nodes.append(iterator)
        iterator = iterator.get_next()

    selected = nodes[position]
    if isinstance(position, slice):
        for node in selected:
            circuit.delete(node)
    else:
        circuit.delete(selected)

    return circuit


machine.finalize()
