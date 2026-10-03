# EVAL_META: task_id=10, framework=cirq, class=3
import cirq

def create_operator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.X(q0),
        cirq.X(q1)
    )
    # Transpile/optimize the circuit using Cirq's target gateset optimizer
    optimized_circuit = cirq.optimize_for_target_gateset(circuit, gateset=cirq.CZTargetGateset())
    return optimized_circuit
