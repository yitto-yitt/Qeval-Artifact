# EVAL_META: task_id=1, framework=cirq, class=1
import cirq

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.measure(q0, q1, key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(x) for x in reversed(row))
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
