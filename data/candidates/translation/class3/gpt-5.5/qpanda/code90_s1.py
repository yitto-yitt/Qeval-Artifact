# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, X, H

def create_custom_controlled():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(4)

    qc2 = QCircuit()
    qc2 << X(qubits[1]).control([qubits[0], qubits[3]])
    qc2 << H(qubits[2]).control([qubits[0], qubits[3]])

    create_custom_controlled._machine = machine
    create_custom_controlled._qubits = qubits
    return qc2
