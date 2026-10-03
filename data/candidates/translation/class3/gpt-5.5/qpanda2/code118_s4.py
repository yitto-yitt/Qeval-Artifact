# EVAL_META: task_id=118, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    sx_matrix = [
        0.5 + 0.5j, 0.5 - 0.5j,
        0.5 - 0.5j, 0.5 + 0.5j
    ]
    circuit = QCircuit()
    circuit.insert(QOracle([q[3]], sx_matrix).control([q[0], q[1], q[2]]))
    return circuit

atexit.register(machine.finalize)
