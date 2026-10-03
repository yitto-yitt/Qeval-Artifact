# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(10)
c = machine.cAlloc_many(10)

def remove_gate_in_position(circuit, position):
    new_circuit = QCircuit()
    seq = circuit.get_sequence()
    n = len(seq)
    if position < 0:
        position += n
    for i, node in enumerate(seq):
        if i == position:
            continue
        new_circuit.insert(node)
    return new_circuit

machine.finalize()
