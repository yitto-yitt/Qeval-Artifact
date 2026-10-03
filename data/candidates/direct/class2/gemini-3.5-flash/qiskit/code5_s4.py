# EVAL_META: task_id=5, framework=qiskit, class=2

from qiskit import QuantumCircuit

def create_state_prep():
    # Create a 2-qubit quantum circuit
    qc = QuantumCircuit(2)
    # In Qiskit, the bitstring "01" corresponds to q1=0, q0=1.
    # Therefore, we apply an X gate to qubit 0.
    qc.x(0)
    return qc
