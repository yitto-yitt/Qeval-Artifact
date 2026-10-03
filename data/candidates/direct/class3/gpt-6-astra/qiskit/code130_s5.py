# EVAL_META: task_id=130, framework=qiskit, class=3
from qiskit import QuantumCircuit


def inv_circuit(n):
    circuit = QuantumCircuit(n)
    circuit.h(1)
    circuit.h(2)
    circuit.cx(1, 3)
    circuit.cx(2, 4)
    return circuit.inverse()
