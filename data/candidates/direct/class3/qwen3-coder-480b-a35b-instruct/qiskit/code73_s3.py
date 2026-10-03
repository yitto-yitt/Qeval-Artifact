# EVAL_META: task_id=73, framework=qiskit, class=3
from qiskit import QuantumCircuit


def x_measurement(circuit, qubit, clbit):
    """
    Adds an X-basis measurement on qubit at index `qubit`, storing the result to classical bit `clbit`.
    
    Args:
        circuit: QuantumCircuit object
        qubit: qubit index to measure
        clbit: classical bit index to store result
        
    Returns:
        None (modifies circuit in place)
    """
    # To measure in X basis, we need to rotate from X basis to Z basis,
    # which means applying H gate before measuring
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
    # Optionally, we could apply another H to rotate back if needed,
    # but for measurement purposes, the above is sufficient
