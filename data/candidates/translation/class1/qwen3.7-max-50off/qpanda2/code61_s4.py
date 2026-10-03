# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import QCircuit, qalloc, calloc, Measure

def create_quantum_circuit_with_one_qubit_and_measure():
    q = qalloc(1)
    c = calloc(1)
    cir = QCircuit()
    cir << Measure(q[0], c[0])
    return cir
