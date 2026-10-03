# EVAL_META: task_id=56, framework=cirq, class=1
import cirq
from collections import Counter

def not_gate(a):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['result']
    counts = Counter()
    for measurement in measurements:
        bitstring = ''.join(map(str, measurement))
        counts[bitstring] += 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
