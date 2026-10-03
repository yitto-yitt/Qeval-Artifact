# EVAL_META: task_id=70, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CSWAP(q[0], q[1], q[2]),
        cirq.H(q[1]),
        cirq.ControlledGate(cirq.S**-1).on(q[1], q[0])
    )
    return circuit
