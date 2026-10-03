# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            circuit.append(cirq.X(qubits[i]))
    
    circuit.append(cirq.measure(*qubits[::-1], key='meas'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    counts = {}
    for row in result.measurements['meas']:
        s = ''.join(str(b) for b in row)
        counts[s] = counts.get(s, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
