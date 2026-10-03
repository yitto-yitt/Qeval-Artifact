# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import ClassicalBit, Measure, QuantumCircuit, Qubit


def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit()
    c = ClassicalBit()
    qc = QuantumCircuit()
    qc << Measure(q, c)
    return qc
