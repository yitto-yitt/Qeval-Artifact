# EVAL_META: task_id=9, framework=cirq, class=3
import cirq

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()

    # Layer of RY rotations
    circuit.append([cirq.ry(0).on(q) for q in qubits])

    # Entangling layer: CNOTs between adjacent qubits
    for i in range(2):
        circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))

    # Barrier
    circuit.append(cirq.Moment())

    # Repetition (reps=1 means one full block, already done above, so nothing more is added)
    # Note: EfficientSU2 with reps=1 applies one block of RY + entanglement.
    # With insert_barriers=True, barriers are placed between layers.
    # Since we only have one block, the barrier at the end is sufficient.

    return circuit
