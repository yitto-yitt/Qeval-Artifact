# EVAL_META: task_id=61, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def create_quantum_circuit_with_one_qubit_and_measure():
    q = QuantumRegister(1, "q")
    c = ClassicalRegister(1, "c")
    circuit = QuantumCircuit(q, c)
    circuit.measure(q, c)
    return circuit
