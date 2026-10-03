# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    circuit = QCircuit()
    gate = U3(q[1], 0.3, 0.2, 0.1)
    controlled_gate = gate.control([q[0]])
    circuit << controlled_gate
    return circuit

machine.finalize()
