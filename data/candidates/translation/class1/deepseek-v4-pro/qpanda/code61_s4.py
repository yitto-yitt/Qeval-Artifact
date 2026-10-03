# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit

def create_quantum_circuit_with_one_qubit_and_measure():
    qc = QuantumCircuit()
    q = qc.qalloc(1)
    c = qc.calloc(1)
    qc.measure(q[0], c[0])
    return qc
