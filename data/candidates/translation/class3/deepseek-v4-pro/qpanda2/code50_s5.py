# EVAL_META: task_id=50, framework=qpanda2, class=3

from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    nodes = list(circuit.get_children())
    del nodes[position]
    circuit.clear()
    for node in nodes:
        circuit.pushBackNode(node)
    return circuit

machine.finalize()
