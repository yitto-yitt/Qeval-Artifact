# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    circuit = QCircuit()
    circuit << RY(q[1], 0.2).control(q[0])
    circuit << X(q[2])
    return circuit

if __name__ == "__main__":
    machine.finalize()
