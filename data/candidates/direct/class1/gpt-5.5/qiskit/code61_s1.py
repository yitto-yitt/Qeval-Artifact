# EVAL_META: task_id=61, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def create_quantum_circuit_with_one_qubit_and_measure():
    qreg = QuantumRegister(1, "q")
    creg = ClassicalRegister(1, "c")
    circuit = QuantumCircuit(qreg, creg)
    circuit.measure(qreg, creg)
    return circuit
