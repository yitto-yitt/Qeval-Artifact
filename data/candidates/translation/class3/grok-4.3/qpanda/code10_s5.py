# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, X

def create_operator():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << X(qubits[0]) << X(qubits[1])
    prog = QProg()
    prog << circuit
    return prog
