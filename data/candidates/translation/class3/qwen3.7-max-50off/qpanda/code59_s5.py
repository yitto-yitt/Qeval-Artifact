# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, QMachine, H, CNOT

def create_cz_gate():
    qm = QMachine()
    q = qm.qAlloc_many(2)
    circuit = QuantumCircuit()
    circuit << H(q[1])
    circuit << CNOT(q[0], q[1])
    circuit << H(q[1])
    return circuit
