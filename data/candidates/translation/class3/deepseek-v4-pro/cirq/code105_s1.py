# EVAL_META: task_id=105, framework=cirq, class=3
import cirq


def initialize_cnot_dihedral():
    """Return a cirq.Circuit that matches the Qiskit CNOTDihedral initialization."""
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.CX(qubits[0], qubits[1]),
        cirq.T(qubits[0]),
    )
    return circuit
