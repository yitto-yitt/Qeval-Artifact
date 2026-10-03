# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CU3

def controlled_custom_unitary_circuit():
    qc = QCircuit()
    qubits = qc.qAllocMany(2)
    qc << CU3(qubits[0], qubits[1], 0.3, 0.2, 0.1)
    return qc
