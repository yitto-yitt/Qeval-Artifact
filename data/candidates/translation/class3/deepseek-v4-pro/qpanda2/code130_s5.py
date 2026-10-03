# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def inv_circuit(n):
    if n < 5:
        raise ValueError("n must be at least 5")

    circuit = QCircuit()
    circuit << CNOT(q[2], q[4])
    circuit << CNOT(q[1], q[3])
    circuit << H(q[2])
    circuit << H(q[1])
    return circuit

machine.finalize()
