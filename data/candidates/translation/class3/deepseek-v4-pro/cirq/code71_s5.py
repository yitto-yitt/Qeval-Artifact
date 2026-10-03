# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    q = cirq.LineQubit.range(3)
    csx = cirq.XPowGate(exponent=0.5).controlled(1)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        csx.on(q[0], q[1]),
        cirq.H(q[1]),
    )
    return circuit
