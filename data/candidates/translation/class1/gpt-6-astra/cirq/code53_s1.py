# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    for value in (a, b):
        for i, qubit in enumerate(qubits):
            if (value >> i) & 1:
                circuit.append(cirq.X(qubit))
    circuit.append(cirq.measure(*reversed(qubits), key="meas"))
    result = cirq.Simulator().run(circuit, repetitions=1024)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(key, "08b"): value / total for key, value in counts.items()}
