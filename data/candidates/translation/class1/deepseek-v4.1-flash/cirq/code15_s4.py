# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import collections

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.depolarize(0.001).on(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.depolarize(0.01, n=2).on(q0, q1))
    circuit.append(cirq.bit_flip(0.02).on(q0))
    circuit.append(cirq.bit_flip(0.02).on(q1))
    circuit.append(cirq.measure(q0, q1, key='m'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1000)
    counts = collections.Counter()
    for b0, b1 in result.measurements['m']:
        bitstring = f"{int(b1)}{int(b0)}"
        counts[bitstring] += 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
