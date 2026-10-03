# EVAL_META: task_id=56, framework=cirq, class=1
import cirq
from collections import Counter

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7 - i] == "0":
            circuit.append(cirq.X(qubits[i]))
    measurement_order = [qubits[7 - i] for i in range(8)]
    circuit.append(cirq.measure(*measurement_order, key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    measurements = result.measurements['m']
    counts = Counter(''.join(str(b) for b in row) for row in measurements)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
