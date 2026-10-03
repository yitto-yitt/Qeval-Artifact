# EVAL_META: task_id=56, framework=cirq, class=1
import cirq
import numpy as np

def not_gate(a):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7 - i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key="result"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key="result")
    total = sum(counts.values())
    formatted_counts = {}
    for k, v in counts.items():
        bitstring = format(k, "08b")
        formatted_counts[bitstring] = v / total
    return formatted_counts
