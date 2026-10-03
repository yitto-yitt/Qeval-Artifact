# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    circuit = QCircuit()
    custom_gate = U3(q[1], 0.3, 0.2, 0.1).control(q[0])
    circuit << custom_gate
    return circuit

machine.finalize()
