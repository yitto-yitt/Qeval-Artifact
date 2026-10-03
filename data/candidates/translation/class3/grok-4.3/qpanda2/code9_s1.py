# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
def create_efficientSU2():
    circuit = QCircuit()
    params = [var(f"theta_{i}") for i in range(12)]
    for i in range(3):
        circuit << RY(q[i], params[2 * i]) << RZ(q[i], params[2 * i + 1])
    circuit << BARRIER(q)
    circuit << CNOT(q[2], q[1]) << CNOT(q[1], q[0])
    circuit << BARRIER(q)
    for i in range(3):
        circuit << RY(q[i], params[6 + 2 * i]) << RZ(q[i], params[6 + 2 * i + 1])
    return circuit
machine.finalize()
