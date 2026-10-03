# EVAL_META: task_id=70, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cswap(0, 1, 2)
    circuit.h(1)
    circuit.csdg(1, 0)
    return circuit
