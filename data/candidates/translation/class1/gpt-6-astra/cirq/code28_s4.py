# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    phi_plus = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q1, q0, key="meas"),
    )
    phi_minus = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q1, q0, key="meas"),
    )
    simulator = cirq.Simulator()
    distributions = {}
    for name, circuit in (("phi_plus", phi_plus), ("phi_minus", phi_minus)):
        result = simulator.run(circuit, repetitions=1000)
        counts = result.histogram(key="meas")
        total = sum(counts.values())
        distributions[name] = {
            format(key, "02b"): count / total for key, count in counts.items()
        }
    return distributions
