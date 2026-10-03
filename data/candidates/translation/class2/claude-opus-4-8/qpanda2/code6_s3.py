# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, X


def create_state_prep(num_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qalloc(num_qubits)

    circuit = QCircuit()
    circuit << X(qubits[0])

    return circuit
