# EVAL_META: task_id=24, framework=cirq, class=1
import cirq


def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    input_qubits = qubits[:-1]
    output_qubit = qubits[-1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(oracle.all_operations())
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.measure(*input_qubits, key='c'))

    shots = 8192
    result = cirq.Simulator().run(circuit, repetitions=shots)
    meas = result.measurements['c']

    counts = {}
    for row in meas:
        bits = ''.join(str(int(b)) for b in row[::-1])
        counts[bits] = counts.get(bits, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
