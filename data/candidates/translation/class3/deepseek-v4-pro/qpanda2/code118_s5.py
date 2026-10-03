# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circuit = QCircuit()
    circuit << C3SX(q[0], q[1], q[2], q[3])
    return circuit

machine.finalize()

