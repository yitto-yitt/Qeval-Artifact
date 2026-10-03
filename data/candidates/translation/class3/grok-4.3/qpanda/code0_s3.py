# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg
def create_quantum_circuit(n_qubits):
    qvm = CPUQVM()
    qvm.init()
    qvm.qAlloc_many(n_qubits)
    return QProg()
