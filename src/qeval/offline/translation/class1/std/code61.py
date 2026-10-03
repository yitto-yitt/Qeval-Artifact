# EVAL_META: task_id=61, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


def create_quantum_circuit_with_one_qubit_and_measure():
    q = QuantumRegister(1, "q")
    c = ClassicalRegister(1, "c")
    qc = QuantumCircuit(q, c)
    qc.measure(q, c)
    return qc
