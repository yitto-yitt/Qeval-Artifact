# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml

def qft_no_swaps(num_qubits):
    """
    Return a callable that applies the inverse Quantum Fourier Transform
    without the final swap gates.
    
    Args:
        num_qubits (int): number of qubits
    
    Returns:
        callable: a quantum function that can be used inside a QNode
    """
    def circuit():
        qml.adjoint(qml.QFT(wires=range(num_qubits), do_swaps=False))
    return circuit
