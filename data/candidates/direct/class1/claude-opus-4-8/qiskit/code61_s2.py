# EVAL_META: task_id=61, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def create_quantum_circuit_with_one_qubit_and_measure():
    qr = QuantumRegister(1, "q")
    cr = ClassicalRegister(1, "c")
    circuit = QuantumCircuit(qr, cr)
    circuit.measure(qr, cr)
    return circuit
