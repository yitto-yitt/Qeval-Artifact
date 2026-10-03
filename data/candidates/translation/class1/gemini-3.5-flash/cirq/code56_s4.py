# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['m']
    
    counts = {}
    for row in measurements:
        bitstring = "".join(str(b) for b in reversed(row))
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
