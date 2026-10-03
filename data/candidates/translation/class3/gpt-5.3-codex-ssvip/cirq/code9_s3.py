# EVAL_META: task_id=9, framework=cirq, class=3
import cirq


def create_efficientSU2():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()

    # Layer 0: single-qubit SU2 rotations (Ry, Rz)
    for qubit in q:
        circuit.append(cirq.ry(0.0)(qubit))
        circuit.append(cirq.rz(0.0)(qubit))

    # Entanglement layer (linear): CX(0,1), CX(1,2)
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.CNOT(q[1], q[2]))

    # Barrier equivalent
    circuit.append(cirq.Moment())

    # Layer 1: single-qubit SU2 rotations (Ry, Rz)
    for qubit in q:
        circuit.append(cirq.ry(0.0)(qubit))
        circuit.append(cirq.rz(0.0)(qubit))

    return circuit
