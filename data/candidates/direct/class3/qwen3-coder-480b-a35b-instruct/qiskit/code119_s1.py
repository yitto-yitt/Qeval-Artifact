# EVAL_META: task_id=119, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import CDKMRippleCarryAdder

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    """Create a quantum circuit with a CDKMRippleCarryAdder.
    
    Args:
        num_state_qubits (int): The number of qubits in each input register.
        kind (str): The type of adder ('half', 'full', or 'fixed').
        
    Returns:
        QuantumCircuit: A quantum circuit with the ripple carry adder applied.
    """
    # Create the ripple carry adder
    adder = CDKMRippleCarryAdder(num_state_qubits, kind=kind)
    
    # Create a circuit with the correct number of qubits
    qc = QuantumCircuit(adder.num_qubits)
    
    # Add the adder to the circuit
    qc.append(adder, range(adder.num_qubits))
    
    return qc
