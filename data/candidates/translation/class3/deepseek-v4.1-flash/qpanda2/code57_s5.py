# EVAL_META: task_id=57, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qv = machine.qAlloc_many(2)

def create_swap_gate():
    circuit = QCircuit()
    circuit << CNOT(qv[0], qv[1])
    circuit << CNOT(qv[1], qv[0])
    circuit << CNOT(qv[0], qv[1])
    return circuit

machine.finalize()
