# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit

def controlled_custom_unitary_circuit():
    # Create 2-qubit circuit
    qc = QuantumCircuit(2)
    # Define custom 1-qubit unitary gate using u3 with angles 0.3, 0.2, 0.1
    custom_unitary_qc = QuantumCircuit(1)
    custom_unitary_qc.u3(0.3, 0.2, 0.1)  # theta, phi, lambda
    custom_gate = custom_unitary_qc.to_gate(label="U_custom")
    # Apply controlled gate: qubit 0 control, qubit 1 target
    qc.append(custom_gate.control(), [0, 1])
    return qc
