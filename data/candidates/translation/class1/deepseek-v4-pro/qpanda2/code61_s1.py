# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import QCircuit, qAlloc, cAlloc, Measure, init


def create_quantum_circuit_with_one_qubit_and_measure():
    init()
    q = qAlloc(1)
    c = cAlloc(1)
    qc = QCircuit()
    qc << Measure(q[0], c[0])
    return qc
