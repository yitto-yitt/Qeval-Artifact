# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def create_cy_gate():
    qc = QCircuit()
    q = qc.allocate_qubits(2)
    qc.sdag(q[1])
    qc.cx(q[0], q[1])
    qc.s(q[1])
    return qc
