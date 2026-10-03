# EVAL_META: task_id=71, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.csx(0, 1)
    circuit.h(1)
    return circuit
