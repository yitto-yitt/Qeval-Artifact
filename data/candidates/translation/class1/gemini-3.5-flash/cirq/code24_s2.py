# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(oracle)
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.measure(*qubits[:-1], key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['result']
    
    counts = {}
    for row in measurements:
        bitstring = "".join(str(b) for b in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
