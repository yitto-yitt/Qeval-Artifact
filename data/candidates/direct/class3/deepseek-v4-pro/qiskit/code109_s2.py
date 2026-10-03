# EVAL_META: task_id=109, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit, Parameter


def circuit():
    """Create a parameterized circuit on one qubit covering the equator."""
    theta = Parameter("θ")
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.p(theta, 0)
    return qc
