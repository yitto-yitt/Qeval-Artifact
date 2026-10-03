# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
import numpy as np

def xor_gate(a, b):
    n = 8
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    # Apply XOR pattern with integer a
    for i in range(n):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    # Apply XOR pattern with integer b
    for i in range(n):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))

    circuit.append(cirq.measure(*qubits, key='result'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    return {f"{k:08b}": v / total for k, v in counts.items()}
