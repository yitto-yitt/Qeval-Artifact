# EVAL_META: task_id=84, framework=cirq, class=3
import cirq

def controlled_custom_unitary_circuit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    custom_gate = cirq.PhasedXZGate.from_zyz_angles(0.3, 0.2, 0.1)
    circuit.append(custom_gate.on(q1).controlled_by(q0))
    return circuit
