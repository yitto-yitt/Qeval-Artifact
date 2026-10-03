# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()

    # First circuit: CX(0, 1), T(0)
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.T(qubits[0]))

    # Second circuit: CX(0, 1), T(0), X(1)
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.T(qubits[0]))
    circuit.append(cirq.X(qubits[1]))

    return circuit
