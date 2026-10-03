# EVAL_META: task_id=3, framework=qiskit, class=2
from qiskit import QuantumCircuit


def create_ghz(drawing=False):
    """Create a 3-qubit GHZ state circuit and measure all qubits."""
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.measure(range(3), range(3))

    if drawing:
        return qc, qc.draw("mpl")
    return qc
