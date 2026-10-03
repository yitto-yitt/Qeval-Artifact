# EVAL_META: task_id=125, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Gate

def circ_to_gate(circ: QuantumCircuit) -> Gate:
    """Convert a QuantumCircuit into a gate equivalent to the action of the input circuit.

    Args:
        circ (QuantumCircuit): The input quantum circuit.

    Returns:
        Gate: The gate representation of the circuit.
    """
    return circ.to_gate()
