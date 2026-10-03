# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()
    
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            circuit.append(cirq.X(qubits[i]))
    
    circuit.append(cirq.measure(*qubits, key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    
    measurements = result.histogram(key='result')
    total = sum(measurements.values())
    
    prob_dist = {}
    for outcome, count in measurements.items():
        binary_str = format(outcome, '08b')
        prob_dist[binary_str] = count / total
    
    return prob_dist
