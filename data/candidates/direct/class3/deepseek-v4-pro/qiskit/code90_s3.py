# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_custom_controlled():
    # Custom 2-qubit gate: X on target 0, H on target 1
    custom_circuit = QuantumCircuit(2, name="XH")
    custom_circuit.x(0)
    custom_circuit.h(1)
    custom_gate = custom_circuit.to_gate()

    # Add two control qubits
    controlled_gate = custom_gate.control(2)

    # Apply to 4-qubit circuit with controls 0,3 and targets 1,2
    qc = QuantumCircuit(4)
    qc.append(controlled_gate, [0, 3, 1, 2])

    return qc
