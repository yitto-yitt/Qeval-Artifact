# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.H(q0),
        cirq.ControlledGate(cirq.rz(theta)).on(q0, q1),
        cirq.H(q1),
        cirq.ControlledGate(cirq.ry(theta)).on(q1, q0),
    )
