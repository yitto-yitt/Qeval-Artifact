# EVAL_META: task_id=3, framework=qiskit, class=2
from qiskit import QuantumCircuit


def create_ghz(drawing=False):
    """Create a 3-qubit GHZ state and measure all qubits."""
    qc = QuantumCircuit(3, 3)

    # Create GHZ state
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)

    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    if drawing:
        fig = qc.draw("mpl")
        return qc, fig

    return qc
