# EVAL_META: task_id=9, framework=cirq, class=3
import cirq


def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()

    # Initial SU2 layer
    for q in qubits:
        circuit.append(cirq.ry(cirq.Symbol(f"θ_ry_0_{q.x}"))(q))
        circuit.append(cirq.rz(cirq.Symbol(f"θ_rz_0_{q.x}"))(q))

    # Entanglement layer (linear)
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))

    # Barrier equivalent
    circuit.append(cirq.Moment())

    # Final SU2 layer
    for q in qubits:
        circuit.append(cirq.ry(cirq.Symbol(f"θ_ry_1_{q.x}"))(q))
        circuit.append(cirq.rz(cirq.Symbol(f"θ_rz_1_{q.x}"))(q))

    return circuit
