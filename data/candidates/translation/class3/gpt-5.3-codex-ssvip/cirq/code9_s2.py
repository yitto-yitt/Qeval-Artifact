# EVAL_META: task_id=9, framework=cirq, class=3
import cirq


def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()

    # Initial SU2 layer (Ry, Rz on each qubit)
    for q in qubits:
        circuit.append(cirq.ry(0.0)(q))
        circuit.append(cirq.rz(0.0)(q))

    # Entanglement layer (linear: 0-1, 1-2)
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))

    # Final SU2 layer (Ry, Rz on each qubit)
    for q in qubits:
        circuit.append(cirq.ry(0.0)(q))
        circuit.append(cirq.rz(0.0)(q))

    return circuit
