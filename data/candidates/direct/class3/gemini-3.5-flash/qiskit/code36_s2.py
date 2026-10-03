# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit

def bv_function(s: str) -> QuantumCircuit:
    """
    Designs a Bernstein-Vazirani oracle from a bitstring and returns it.
    
    Args:
        s (str): The secret bitstring.
        
    Returns:
        QuantumCircuit: The quantum circuit representing the oracle.
    """
    n = len(s)
    # The circuit has n input qubits and 1 target qubit (at index n)
    qc = QuantumCircuit(n + 1)
    
    # Apply CX gates from input qubits to the target qubit where the bit in s is '1'
    # Following standard Qiskit convention, the rightmost bit of s corresponds to qubit 0.
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(i, n)
            
    return qc
