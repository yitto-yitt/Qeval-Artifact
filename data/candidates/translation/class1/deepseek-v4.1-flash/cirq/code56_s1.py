# EVAL_META: task_id=56, framework=cirq, class=1
import cirq

def not_gate(a):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()
    for i in range(8):
        if (a >> i) & 1 == 0:
            circuit.append(cirq.X(qubits[i]))
    # Measure in order q7...q0 to match Qiskit's key format (leftmost = qubit 7)
    circuit.append(cirq.measure(*[qubits[7 - i] for i in range(8)], key='m'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = {}
    for bits in result.measurements['m']:
        bitstring = ''.join(str(int(b)) for b in bits)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
