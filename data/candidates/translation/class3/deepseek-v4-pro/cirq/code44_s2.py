# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    # Top circuit: 1-qubit with X gate
    q_top = cirq.NamedQubit('q0_0')
    top = cirq.Circuit(cirq.X(q_top))

    # Bottom circuit: 2-qubit with CRY gate (0.2 rad, controlled by qubit 0)
    q0_bot = cirq.NamedQubit('q1_0')
    q1_bot = cirq.NamedQubit('q1_1')
    bottom = cirq.Circuit(cirq.Y(q1_bot) ** (0.2 / cirq.pi)).controlled_by(q0_bot)

    # In Qiskit: tensored = bottom.tensor(top) means bottom comes first, then top
    # Cirq: cirq.Circuit(bottom, top) places bottom before top in moment order,
    # but we need to ensure qubit ordering: bottom qubits first, then top qubits.
    # We'll combine them directly.
    tensored = cirq.Circuit(bottom.all_operations(), top.all_operations())

    return tensored
