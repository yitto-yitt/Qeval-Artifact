# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def simons_algorithm(s):
    q = QuantumRegister(len(s), "q")
    c = ClassicalRegister(len(s), "c")
    circuit = QuantumCircuit(q, c)
    circuit.measure(q, c)
    return circuit
