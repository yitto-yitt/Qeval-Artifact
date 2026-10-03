# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = QCircuit()

    # First rotation layer: Ry then Rz on each qubit
    circuit << RY(q[0], 0.0) << RZ(q[0], 0.0)
    circuit << RY(q[1], 0.0) << RZ(q[1], 0.0)
    circuit << RY(q[2], 0.0) << RZ(q[2], 0.0)

    circuit << BARRIER(q)

    # reverse_linear entanglement layer: CNOT(1,0), CNOT(2,1)
    circuit << CNOT(q[1], q[0])
    circuit << CNOT(q[2], q[1])

    circuit << BARRIER(q)

    # Final rotation layer
    circuit << RY(q[0], 0.0) << RZ(q[0], 0.0)
    circuit << RY(q[1], 0.0) << RZ(q[1], 0.0)
    circuit << RY(q[2], 0.0) << RZ(q[2], 0.0)

    return circuit

machine.finalize()
