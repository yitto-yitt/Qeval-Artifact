# EVAL_META: task_id=59, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_cz_gate():
    circuit = QCircuit()
    circuit.insert(H(q[1]))
    circuit.insert(CNOT(q[0], q[1]))
    circuit.insert(H(q[1]))
    return circuit

machine.finalize()
