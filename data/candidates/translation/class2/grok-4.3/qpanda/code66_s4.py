# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import init_quantum_machine, QMachineType, QProg, RY, CH, CNOT, X, measure_all


def w_state():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    circuit = QProg()
    circuit << RY(q[0], 2 * arccos(1 / sqrt(3)))
    circuit << CH(q[0], q[1])
    circuit << CNOT(q[1], q[2])
    circuit << CNOT(q[0], q[1])
    circuit << X(q[0])
    circuit << measure_all(q, c)
    return circuit
