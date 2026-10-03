# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circuit = QCircuit()

    h1 = H(q[3])
    h1.setControl(q[0])
    h1.setControl(q[1])
    h1.setControl(q[2])
    circuit << h1

    s_gate = S(q[3])
    s_gate.setControl(q[0])
    s_gate.setControl(q[1])
    s_gate.setControl(q[2])
    circuit << s_gate

    h2 = H(q[3])
    h2.setControl(q[0])
    h2.setControl(q[1])
    h2.setControl(q[2])
    circuit << h2

    return circuit

machine.finalize()
