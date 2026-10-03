# EVAL_META: task_id=36, framework=qiskit, class=3

from qiskit import QuantumCircuit

def bv_function(s: str) -> QuantumCircuit:
    """
    Designs a Bernstein-Vazirani oracle from a bitstring and returns it.
    
    Args:
        s (str): The hidden bitstring.
        
    Returns:
        QuantumCircuit: The quantum circuit representing the oracle.
    """
    n = len(s)
    # The oracle acts on n input qubits and 1 target qubit (total n + 1 qubits)
    oracle = QuantumCircuit(n + 1)
    
    # Reverse the bitstring to match Qiskit's LSB-first qubit ordering
    s_reversed = s[::-1]
    for i in range(n):
        if s_reversed[i] == '1':
            oracle.cx(i, n)
            
    return oracle
