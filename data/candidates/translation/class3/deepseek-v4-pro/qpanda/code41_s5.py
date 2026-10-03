# EVAL_META: task_id=41, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Y, X, init_quantum_machine, QMachineType


def compose_op():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(3)
    circuit = QCircuit()
    circuit << Y(q[0])
    circuit << X(q[2])
    return circuit
