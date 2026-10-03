# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    custom = QCircuit()
    custom.insert(X(q[1]))
    custom.insert(H(q[2]))

    controlled_custom = custom.control([q[0], q[3]])

    circuit = QCircuit()
    circuit.insert(controlled_custom)
    return circuit

machine.finalize()
