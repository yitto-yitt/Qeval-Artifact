# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, X

def create_state_prep():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << X(qubits[0])
    return circuit
