# EVAL_META: task_id=119, framework=qiskit, class=3
from qiskit.circuit.library import CDKMRippleCarryAdder

def create_ripple_carry_adder_circuit(num_state_qubits: int, kind: str) -> CDKMRippleCarryAdder:
    """Create a CDKMRippleCarryAdder circuit.

    Args:
        num_state_qubits (int): The number of qubits in each of the two input registers.
        kind (str): The kind of adder, can be 'full', 'half', or 'fixed'.

    Returns:
        CDKMRippleCarryAdder: The ripple carry adder circuit.
    """
    return CDKMRippleCarryAdder(num_state_qubits, kind=kind)
