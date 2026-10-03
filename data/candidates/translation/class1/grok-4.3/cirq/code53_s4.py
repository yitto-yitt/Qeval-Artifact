# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    for i in range(8):
        if (a & (1 << i)) != 0:
            circuit.append(cirq.X(qubits[i]))
        if (b & (1 << i)) != 0:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='meas'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    return {format(key, '08b'): value / total for key, value in counts.items()}
