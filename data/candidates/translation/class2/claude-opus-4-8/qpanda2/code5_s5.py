# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, X


def create_state_prep():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << X(qubits[1])
    return circuit
