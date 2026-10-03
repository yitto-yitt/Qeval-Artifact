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
    # Reverse the row to match Qiskit's little-endian bitstring ordering (q_N ... q_1 q_0)
    bitstrings = [''.join(str(int(b)) for b in reversed(row)) for row in measurements]
    
    counts = Counter(bitstrings)
    total = sum(counts.values())
    
    return {k: v / total for k, v in counts.items()}
