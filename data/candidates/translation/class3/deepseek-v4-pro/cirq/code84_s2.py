# EVAL_META: task_id=84, framework=cirq, class=3
import cirq

def controlled_custom_unitary_circuit():
    q0, q1 = cirq.LineQubit.range(2)
    custom_gate = cirq.MatrixGate(cirq.unitary(cirq.cirq_u3(0.3, 0.2, 0.1)))
    controlled_gate = custom_gate.controlled()
    circuit = cirq.Circuit(controlled_gate(q0, q1))
    return circuit
