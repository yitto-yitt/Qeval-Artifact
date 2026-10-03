# EVAL_META: task_id=5, framework=qiskit, class=2

from qiskit import QuantumCircuit

def create_state_prep():
    # In Qiskit, the bitstring "01" corresponds to |01> where q1 = 0 and q0 = 1.
    # Therefore, we apply an X gate to qubit 0.
    qc = QuantumCircuit(2)
    qc.x(0)
    return qc
