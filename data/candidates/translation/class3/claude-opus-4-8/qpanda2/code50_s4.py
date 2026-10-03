# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def remove_gate_in_position(circuit, position):
    nodes = list(circuit)
    new_circuit = QCircuit()
    for i, node in enumerate(nodes):
        if i != position:
            new_circuit.insert(node)
    return new_circuit

machine.finalize()
