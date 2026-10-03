# EVAL_META: task_id=61, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def create_quantum_circuit_with_one_qubit_and_measure():
    quantum_register = QuantumRegister(1, "q")
    classical_register = ClassicalRegister(1, "c")
    circuit = QuantumCircuit(quantum_register, classical_register)
    circuit.measure(quantum_register[0], classical_register[0])
    return circuit
