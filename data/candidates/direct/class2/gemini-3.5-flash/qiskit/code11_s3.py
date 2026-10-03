# EVAL_META: task_id=11, framework=qiskit, class=2

from qiskit.quantum_info import Statevector

def get_statevector(circuit):
    """
    Compute and return the statevector corresponding to the input circuit.
    
    Args:
        circuit (QuantumCircuit): The input quantum circuit.
        
    Returns:
        Statevector: The Statevector object representing the output state of the circuit.
    """
    return Statevector(circuit)
