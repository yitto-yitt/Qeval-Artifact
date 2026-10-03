# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit import QuantumCircuit

def mcy(qc):
    # Implement multi-controlled Y gate using multi-controlled X gate with S gates
    # MCY = S† * MCX * S where control is on all control qubits
    qc.sdg(4)  # Apply S† to target qubit
    qc.mcx([0, 1, 2, 3], 4)  # Multi-controlled X gate
    qc.s(4)  # Apply S to target qubit
    return qc
