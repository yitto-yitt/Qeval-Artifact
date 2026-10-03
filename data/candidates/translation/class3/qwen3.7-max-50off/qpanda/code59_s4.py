# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_cz_gate():
    qc = QuantumCircuit(2)
    q = qc.qubits
    qc.h(q[1])
    qc.cx(q[0], q[1])
    qc.h(q[1])
    return qc
