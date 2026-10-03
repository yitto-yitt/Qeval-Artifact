# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)

def remove_gate_in_position(circuit, position):
    seq = circuit.get_sequence()
    del seq[position]
    circuit.set_sequence(seq)
    return circuit

machine.finalize()
