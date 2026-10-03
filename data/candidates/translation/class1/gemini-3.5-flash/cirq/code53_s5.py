# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a: int, b: int):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    
    for i in range(8):
        if ((a ^ b) >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    circuit.append(cirq.measure(*qubits, key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=100)
    
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(x) for x in reversed(row))
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
