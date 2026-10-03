# EVAL_META: task_id=60, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_cy_gate():
    circuit = QCircuit()
    circuit << Sdg(q[1]) << CNOT(q[0], q[1]) << S(q[1])
    return circuit

atexit.register(machine.finalize)
