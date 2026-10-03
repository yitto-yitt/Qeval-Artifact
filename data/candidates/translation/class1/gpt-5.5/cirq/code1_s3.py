# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
from collections import Counter

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    measurements = result.measurements["meas"]
    counts = Counter("".join(str(int(bit)) for bit in row) for row in measurements)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
