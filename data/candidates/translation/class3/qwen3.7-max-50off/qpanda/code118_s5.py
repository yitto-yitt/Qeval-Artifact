# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, SX

def create_c3sx_circuit():
    qc = QCircuit()
    q = qc.alloc_qubits(4)
    c3sx_gate = SX(q[3]).control([q[0], q[1], q[2]])
    qc << c3sx_gate
    return qc
