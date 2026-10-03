# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
import collections

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    measurements = result.measurements['meas']
    counts = collections.Counter()
    for row in measurements:
        bitstring = ''.join(str(int(bit)) for bit in row[::-1])
        counts[bitstring] += 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
