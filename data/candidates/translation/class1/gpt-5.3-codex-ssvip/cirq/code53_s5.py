# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a, b):
    qubits = [cirq.LineQubit(i) for i in range(8)]
    circuit = cirq.Circuit()

    for i, q in enumerate(qubits):
        if (a >> i) & 1:
            circuit.append(cirq.X(q))
    for i, q in enumerate(qubits):
        if (b >> i) & 1:
            circuit.append(cirq.X(q))

    circuit.append(cirq.measure(*qubits, key='meas'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    hist = result.multi_measurement_histogram(keys=['meas'])
    total = sum(hist.values())

    probs = {}
    for bits_tuple, count in hist.items():
        bitstring = ''.join(str(bit) for bit in bits_tuple[::-1])
        probs[bitstring] = count / total
    return probs
