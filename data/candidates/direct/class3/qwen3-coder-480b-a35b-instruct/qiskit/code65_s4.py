# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT as qiskit_qft


def QFT(n):
    qc = QuantumCircuit(n)
    
    # Apply Hadamard gate to each qubit starting from the first
    for i in range(n):
        qc.h(i)
        
        # Apply controlled phase shift gates to subsequent qubits
        for j in range(2, n - i + 1):
            angle = 2 * 3.141592653589793 / (2 ** j)
            qc.cp(angle, i + j - 1, i)
    
    # Reverse the order of qubits to complete the QFT
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    
    return qc
