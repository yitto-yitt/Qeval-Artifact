# EVAL_META: task_id=1, framework=cirq, class=1
import cirq

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.measure(q0, q1, key='meas'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.multi_measurement_histogram(keys=['meas'])
    total = sum(counts.values())
    dist = {}
    for key, value in counts.items():
        bitstring = ''.join(str(b) for b in key)
        dist[bitstring] = value / total
    return dist
