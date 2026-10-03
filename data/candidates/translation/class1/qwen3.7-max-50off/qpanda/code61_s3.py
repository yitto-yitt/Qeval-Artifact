# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QuantumRegister, ClassicalRegister, QuantumCircuit, Measure

def create_quantum_circuit_with_one_qubit_and_measure():
    q = QuantumRegister(1, "q")
    c = ClassicalRegister(1, "c")
    qc = QuantumCircuit(q, c)
    qc << Measure(q[0], c[0])
    return qc
