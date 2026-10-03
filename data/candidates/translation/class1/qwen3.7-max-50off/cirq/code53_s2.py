# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    for i in range(8):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    circuit.append(cirq.measure(*qubits, key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['m']
    
    counts = {}
    for row in measurements:
        bitstring = ''.join(str(int(bit)) for bit in row[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
