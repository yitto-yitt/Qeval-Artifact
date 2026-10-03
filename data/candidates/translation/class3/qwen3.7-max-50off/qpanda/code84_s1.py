# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def controlled_custom_unitary_circuit():
    qc = QuantumCircuit(2)
    qc.cu3(0.3, 0.2, 0.1, 0, 1)
    return qc
