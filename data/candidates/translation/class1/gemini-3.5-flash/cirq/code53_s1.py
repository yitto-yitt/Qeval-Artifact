# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
import collections

def xor_gate(a: int, b: int):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()
    
    xor_val = a ^ b
    for i in range(8):
        if (xor_val >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    measured_qubits = qubits[::-1]
    circuit.append(cirq.measure(*measured_qubits, key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    measurements = result.measurements['m']
    counts = collections.Counter()
    for row in measurements:
        bitstring = "".join(str(x) for x in row)
        counts[bitstring] += 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
