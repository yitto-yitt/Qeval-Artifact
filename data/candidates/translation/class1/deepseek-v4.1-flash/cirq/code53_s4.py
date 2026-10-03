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
    measurement_qubits = [qubits[7 - i] for i in range(8)]
    circuit.append(cirq.measure(*measurement_qubits, key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=100)
    counts = result.measurements['m']
    bitstrings = [''.join(str(b) for b in row) for row in counts]
    count_dict = {}
    for bs in bitstrings:
        count_dict[bs] = count_dict.get(bs, 0) + 1
    total = sum(count_dict.values())
    return {k: v / total for k, v in count_dict.items()}
