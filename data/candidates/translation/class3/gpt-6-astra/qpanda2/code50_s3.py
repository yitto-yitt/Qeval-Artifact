# EVAL_META: task_id=50, framework=qpanda2, class=3
import operator
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def remove_gate_in_position(circuit, position):
    nodes = []
    iterator = circuit.begin()
    end = circuit.end()

    while iterator != end:
        nodes.append(iterator)
        iterator = iterator.get_next()

    if isinstance(position, slice):
        selected = nodes[position]
        for node in reversed(selected):
            circuit.delete(node)
    else:
        circuit.delete(nodes[operator.index(position)])

    return circuit


machine.finalize()
