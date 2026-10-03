# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    
    for i in range(8):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    
    counts = {}
    for m in result.measurements['meas']:
        bitstring = ''.join(str(bit) for bit in reversed(m))
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
