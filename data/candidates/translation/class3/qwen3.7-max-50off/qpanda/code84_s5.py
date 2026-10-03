# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, U3

def controlled_custom_unitary_circuit():
    qc = QCircuit(2)
    q = qc.qubits
    custom_gate = U3(0.3, 0.2, 0.1)
    controlled_gate = custom_gate.control(1)
    qc << controlled_gate(q[0], q[1])
    return qc
