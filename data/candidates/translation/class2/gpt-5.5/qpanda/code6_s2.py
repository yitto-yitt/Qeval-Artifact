# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, X, I


def create_state_prep(num_qubits):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    circuit = QCircuit()
    if num_qubits > 0:
        circuit << X(qubits[0])
        for i in range(1, num_qubits):
            circuit << I(qubits[i])
    return circuit
