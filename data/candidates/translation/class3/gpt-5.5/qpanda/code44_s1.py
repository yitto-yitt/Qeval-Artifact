# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, X, RY

def tensor_circuits():
    if not hasattr(tensor_circuits, "_machines"):
        tensor_circuits._machines = []
    machine = CPUQVM()
    machine.init()
    tensor_circuits._machines.append(machine)

    q = machine.qAlloc_many(3)
    circuit = QCircuit()
    circuit << RY(q[1], 0.2).control([q[0]])
    circuit << X(q[2])
    return circuit
