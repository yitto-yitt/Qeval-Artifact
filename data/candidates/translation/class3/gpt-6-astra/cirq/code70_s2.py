# EVAL_META: task_id=70, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    q0, q1, q2 = cirq.LineQubit.range(3)
    return cirq.Circuit(
        cirq.H(q0),
        cirq.CSWAP(q0, q1, q2),
        cirq.H(q1),
        (cirq.S ** -1)(q0).controlled_by(q1),
    )
