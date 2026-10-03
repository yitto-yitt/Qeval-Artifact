# EVAL_META: task_id=38, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.crz(theta, 0, 1)
    circuit.h(1)
    circuit.cry(theta, 1, 0)
    return circuit
