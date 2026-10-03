# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, measure


def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit()
    c = CBit()
    qc = QCircuit()
    qc << measure(q, c)
    return qc
