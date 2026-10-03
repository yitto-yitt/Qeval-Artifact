# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
from collections import Counter

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = Counter()
    for sample in result.measurements['m']:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        counts[bitstring] += 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
