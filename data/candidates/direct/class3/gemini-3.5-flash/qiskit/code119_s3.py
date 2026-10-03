# EVAL_META: task_id=119, framework=qiskit, class=3

from qiskit.circuit.library import CDKMRippleCarryAdder

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    """Create a QuantumCircuit with a CDKMRippleCarryAdder applied to the qubits.
    
    Args:
        num_state_qubits (int): The number of qubits in the input registers.
        kind (str): The kind of adder ('full', 'half', or 'fixed').
        
    Returns:
        CDKMRippleCarryAdder: The ripple carry adder circuit.
    """
    return CDKMRippleCarryAdder(num_state_qubits, kind=kind)
