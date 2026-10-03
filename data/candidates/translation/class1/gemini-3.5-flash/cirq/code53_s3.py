# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    for i in range(8):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        if bit_a:
            circuit.append(cirq.X(qubits[7 - i]))
        if bit_b:
            circuit.append(cirq.X(qubits[7 - i]))
    circuit.append(cirq.measure(*qubits, key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    histogram = result.histogram(key='m')
    total = sum(histogram.values())
    return {f"{val:08b}": count / total for val, count in histogram.items()}
