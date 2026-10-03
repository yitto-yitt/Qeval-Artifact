# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    input_qubits = qubits[:-1]
    output_qubit = qubits[-1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H(q) for q in qubits)
    circuit += oracle
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*input_qubits, key='c'))

    shots = 4096
    result = cirq.Simulator().run(circuit, repetitions=shots)
    measurements = result.measurements['c']

    counts = {}
    for row in measurements:
        bitstring = ''.join(str(int(b)) for b in reversed(row))
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
