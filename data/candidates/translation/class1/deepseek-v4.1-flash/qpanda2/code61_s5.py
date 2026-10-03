# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import QCircuit, Qubit, CBit, measure

def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit(0)
    c = CBit(0)
    qc = QCircuit()
    qc << measure(q, c)
    return qc
