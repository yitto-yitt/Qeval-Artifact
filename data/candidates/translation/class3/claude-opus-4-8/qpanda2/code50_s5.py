# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)


def remove_gate_in_position(circuit, position):
    new_circuit = QCircuit()
    nodes = []
    for node in circuit:
        nodes.append(node)
    for i, node in enumerate(nodes):
        if i != position:
            new_circuit << node
    return new_circuit


machine.finalize()
