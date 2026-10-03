# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QProg, CPUQVM, unitary
def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QProg()
    circuit << unitary(qubits, matrix)
    return circuit
