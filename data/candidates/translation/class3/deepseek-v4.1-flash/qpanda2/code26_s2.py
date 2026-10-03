# EVAL_META: task_id=26, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)


def bell_dag():
    circ = QCircuit()
    circ << H(q[0])
    circ << CNOT(q[0], q[1])
    circ << Measure(q[0], c[0])
    return circ


if __name__ == "__main__":
    machine.finalize()
