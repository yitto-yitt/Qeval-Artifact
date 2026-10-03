# EVAL_META: task_id=14, framework=cirq, class=1
import cirq
from collections import Counter

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    # Measure q1 then q0 to match Qiskit's little-endian bitstring representation
    circuit.append(cirq.measure(q1, q0, key='meas'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    
    measurements = result.measurements['meas']
    bitstrings = ["".join(str(bit) for bit in shot) for shot in measurements]
    
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
