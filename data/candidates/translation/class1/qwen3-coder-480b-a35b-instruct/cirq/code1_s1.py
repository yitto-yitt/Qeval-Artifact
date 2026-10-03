# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
import collections

def run_bell_state_simulator():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.measure(*qubits, key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    measurements = result.measurements['result']
    
    counts = collections.Counter()
    for measurement in measurements:
        bitstring = ''.join(str(bit) for bit in measurement)
        counts[bitstring] += 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
