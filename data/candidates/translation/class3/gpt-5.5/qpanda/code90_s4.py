# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    qubits = qvm.qAlloc_many(4)

    custom = QCircuit()
    custom << X(qubits[1])
    custom << H(qubits[2])

    controls = [qubits[0], qubits[3]]
    controlled_custom = custom.control(controls) if hasattr(custom, "control") else custom.set_control(controls)
    if controlled_custom is None:
        controlled_custom = custom

    qc = QCircuit()
    qc << controlled_custom

    globals()["_create_custom_controlled_qvm"] = qvm
    globals()["_create_custom_controlled_qubits"] = qubits

    return qc
