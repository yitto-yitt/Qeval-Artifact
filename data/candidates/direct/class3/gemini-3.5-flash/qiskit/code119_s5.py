# EVAL_META: task_id=119, framework=qiskit, class=3
from qiskit.circuit.library import CDKMRippleCarryAdder

def create_ripple_carry_adder_circuit(num_state_qubits: int, kind: str):
    """Create a CDKMRippleCarryAdder circuit.

    Args:
        num_state_qubits (int): Number of state qubits.
        kind (str): Kind of adder ('full', 'half', or 'fixed').

    Returns:
        CDKMRippleCarryAdder: The ripple carry adder circuit.
    """
    return CDKMRippleCarryAdder(num_state_qubits, kind=kind)
