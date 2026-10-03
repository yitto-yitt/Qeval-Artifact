# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import Qubit, CBit, QCircuit, QProg


def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit()
    c = CBit()
    qc = QCircuit()
    qc.insert(q.measure(c))
    return qc
