# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    n = 8
    qubits = [cirq.LineQubit(i) for i in range(n)]
    circuit = cirq.Circuit()
    # XOR(a): flip qubit i where bit i of a is set
    for i in range(n):
        if (a >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    # XOR(b): flip qubit i where bit i of b is set
    for i in range(n):
        if (b >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='meas'))

    simulator = cirq.Simulator()
    reps = 1024
    result = simulator.run(circuit, repetitions=reps)
    meas = result.measurements['meas']  # shape (reps, n), order qubit0..qubit7

    counts = {}
    for row in meas:
        # Qiskit string: qubit(n-1) ... qubit0
        key = ''.join(str(int(row[i])) for i in range(n - 1, -1, -1))
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
