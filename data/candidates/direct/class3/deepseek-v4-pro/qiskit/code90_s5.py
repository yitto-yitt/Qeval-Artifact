# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_custom_controlled():
    # Custom 2-qubit gate: X on first target qubit, H on second target qubit
    target_gate = QuantumCircuit(2, name="XH")
    target_gate.x(0)
    target_gate.h(1)
    custom_gate = target_gate.to_gate()

    # Add two control qubits to the custom gate
    controlled_gate = custom_gate.control(2)

    # Apply to 4-qubit circuit:
    # controls: qubits 0, 3; targets: qubits 1, 2
    qc = QuantumCircuit(4)
    qc.append(controlled_gate, [0, 3, 1, 2])

    return qc
