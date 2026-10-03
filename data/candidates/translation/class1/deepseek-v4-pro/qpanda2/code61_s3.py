# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import QCircuit, Measure, cAlloc, qAlloc


def create_quantum_circuit_with_one_qubit_and_measure():
    q = qAlloc()
    c = cAlloc()
    qc = QCircuit()
    qc << Measure(q, c)
    return qc
