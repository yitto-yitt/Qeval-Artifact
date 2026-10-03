# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np


def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        qubits = sorted(oracle.all_qubits())
        n = len(qubits)
    elif isinstance(oracle, cirq.Operation):
        qubits = list(oracle.qubits)
        n = len(qubits)
    else:
        num_qubits = getattr(oracle, "num_qubits", None)
        n = num_qubits() if callable(num_qubits) else num_qubits
        qubits = cirq.LineQubit.range(n)

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[n - 1]))
    circuit.append(cirq.H.on_each(*qubits))

    if isinstance(oracle, cirq.Circuit):
        circuit += oracle
    elif isinstance(oracle, cirq.Operation):
        circuit.append(oracle)
    elif isinstance(oracle, cirq.Gate):
        circuit.append(oracle.on(*qubits))
    else:
        circuit.append(oracle.on(*qubits))

    circuit.append(cirq.H.on_each(*qubits))

    result = cirq.Simulator().simulate(circuit, qubit_order=qubits)
    state = result.final_state_vector

    probabilities = {}
    for index, amplitude in enumerate(state):
        prob = float(abs(amplitude) ** 2)
        if prob <= 1e-12:
            continue
        bits = [(index >> (n - 1 - i)) & 1 for i in range(n)]
        key = "".join(str(bits[i]) for i in range(n - 2, -1, -1))
        probabilities[key] = probabilities.get(key, 0.0) + prob

    total = sum(probabilities.values())
    return {key: value / total for key, value in probabilities.items()}
