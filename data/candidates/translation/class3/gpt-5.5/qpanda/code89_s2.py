# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import *


def create_controlled_hgate():
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    qubits = machine.qAlloc_many(3)
    circuit = QCircuit()

    gate = H(qubits[2]).control([qubits[0], qubits[1]])
    circuit << gate

    create_controlled_hgate._machine = machine
    return circuit
