# EVAL_META: task_id=1, framework=cirq, class=1
import cirq

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    bell = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q1, q0, key="meas"),
    )
    isa_circuit = cirq.optimize_for_target_gateset(
        bell, gateset=cirq.CZTargetGateset()
    )
    result = cirq.Simulator().run(isa_circuit, repetitions=1000)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(key, "02b"): value / total for key, value in counts.items()}
