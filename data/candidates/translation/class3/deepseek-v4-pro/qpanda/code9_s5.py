# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc_many, RY, RZ, CNOT, BARRIER, VarParameter

def create_efficientSU2():
    q = qAlloc_many(3)
    circuit = QCircuit()
    params = [VarParameter(f'theta{i}') for i in range(12)]

    for i in range(3):
        circuit << RY(q[i], params[i])
    for i in range(3):
        circuit << RZ(q[i], params[3 + i])
    circuit << BARRIER(q)

    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[1], q[2])
    circuit << BARRIER(q)

    for i in range(3):
        circuit << RY(q[i], params[6 + i])
    for i in range(3):
        circuit << RZ(q[i], params[9 + i])
    circuit << BARRIER(q)

    return circuit
