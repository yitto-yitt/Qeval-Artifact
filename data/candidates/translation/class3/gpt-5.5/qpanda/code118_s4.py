# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import *


def create_c3sx_circuit():
    machine = CPUQVM()
    try:
        machine.init()
    except AttributeError:
        try:
            machine.init_qvm()
        except AttributeError:
            pass

    qubits = machine.qAlloc_many(4)

    prog = QProg()
    prog << H(qubits[3])
    prog << S(qubits[3]).control([qubits[0], qubits[1], qubits[2]])
    prog << H(qubits[3])

    if not hasattr(create_c3sx_circuit, "_resources"):
        create_c3sx_circuit._resources = []
    create_c3sx_circuit._resources.append((machine, qubits))

    return prog
