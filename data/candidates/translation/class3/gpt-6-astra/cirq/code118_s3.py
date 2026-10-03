# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    return cirq.Circuit(
        cirq.XPowGate(exponent=0.5).controlled(num_controls=3).on(*qubits)
    )
