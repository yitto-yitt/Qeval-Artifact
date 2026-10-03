# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import QuantumCircuit


def create_quantum_circuit_with_one_qubit_and_measure():
    qc = QuantumCircuit(1, 1)
    qc.measure(0, 0)
    return qc
