# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == '0':
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    measurements = result.measurements['m']
    str_counts = {}
    for row in measurements:
        bitstring = "".join(str(int(bit)) for bit in row[::-1])
        str_counts[bitstring] = str_counts.get(bitstring, 0) + 1
        
    total = sum(str_counts.values())
    return {k: v / total for k, v in str_counts.items()}
