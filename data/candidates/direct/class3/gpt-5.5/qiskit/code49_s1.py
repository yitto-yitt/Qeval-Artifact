# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit


def simple_elitzur_vaidman():
    circuit = QuantumCircuit(2, name="simple_elitzur_vaidman")
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.h(0)
    return circuit
