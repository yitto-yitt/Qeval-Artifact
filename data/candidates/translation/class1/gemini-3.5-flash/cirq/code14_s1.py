# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
from collections import Counter

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    measurements = result.measurements['m']
    
    # Qiskit's bitstring is reversed (MSB is qubit 1, LSB is qubit 0)
    bitstrings = [''.join(map(str, row[::-1])) for row in measurements]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
