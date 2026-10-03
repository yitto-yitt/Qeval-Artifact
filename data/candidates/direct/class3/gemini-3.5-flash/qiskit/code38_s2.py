# EVAL_META: task_id=38, framework=qiskit, class=3

from qiskit import QuantumCircuit

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    """
    Builds a 2-qubit Quantum Circuit with:
    - H gate on qubit 0
    - Controlled-RZ gate with control 0 and target 1 with parameter theta
    - H gate on qubit 1
    - Controlled-RY gate with control 1 and target 0 with parameter theta
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.crz(theta, 0, 1)
    qc.h(1)
    qc.cry(theta, 1, 0)
    return qc
