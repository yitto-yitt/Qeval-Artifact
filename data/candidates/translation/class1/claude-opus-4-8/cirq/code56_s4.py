# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()
    a = format(a, "08b")
    for i in range(8):
        if a[7 - i] == "0":
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key="meas"))
    simulator = cirq.Simulator()
    reps = 1024
    result = simulator.run(circuit, repetitions=reps)
    measurements = result.measurements["meas"]
    counts = {}
    for row in measurements:
        key = "".join(str(int(b)) for b in row[::-1])
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
