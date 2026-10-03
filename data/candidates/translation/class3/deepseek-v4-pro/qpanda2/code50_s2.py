# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    if position < 0:
        position += circuit.getQGateNum()
    circuit.deleteQGateByIndex(position)
    return circuit

machine.finalize()
