# EVAL_META: task_id=92, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState

def calculate_stabilizer_state_info() -> dict:
    """
    Constructs a Phi plus Bell state quantum circuit and computes
    the stabilizer state measurement probabilities.
    
    Returns:
        dict: The stabilizer-state probability distribution dictionary.
    """
    # Construct Phi plus Bell state: (|00> + |11>) / sqrt(2)
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    # Create StabilizerState from the circuit
    state = StabilizerState(qc)
    
    # Get the measurement probabilities dictionary
    probabilities = state.probabilities_dict()
    
    return probabilities
