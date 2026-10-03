# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    # Determine the number of qubits and the qubit list
    if isinstance(oracle, cirq.Circuit):
        qubits = sorted(oracle.all_qubits())
        n = len(qubits)
    elif isinstance(oracle, cirq.Gate):
        n = oracle.num_qubits()
        qubits = cirq.LineQubit.range(n)
    elif isinstance(oracle, cirq.Operation):
        qubits = sorted(oracle.qubits)
        n = len(qubits)
    else:
        # Fallback: assume it's a gate-like object with num_qubits method
        if hasattr(oracle, 'num_qubits'):
            n = oracle.num_qubits() if callable(oracle.num_qubits) else oracle.num_qubits
        else:
            raise ValueError("Unsupported oracle type")
        qubits = cirq.LineQubit.range(n)

    output_qubit = qubits[-1]
    input_qubits = qubits[:-1]
    n = len(qubits)

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H.on_each(*qubits))

    if isinstance(oracle, cirq.Circuit):
        circuit.append(oracle)
    elif isinstance(oracle, cirq.Gate):
        circuit.append(oracle.on(*qubits))
    elif isinstance(oracle, cirq.Operation):
        circuit.append(oracle)
    else:
        circuit.append(oracle.on(*qubits))

    circuit.append(cirq.H.on_each(*qubits))

    simulator = cirq.Simulator()
    state = simulator.simulate(circuit).final_state_vector

    input_size = n - 1
    probs = {}
    if input_size == 0:
        return {'': 1.0}

    for K in range(2**input_size):
        v = [ (K >> i) & 1 for i in range(input_size) ]
        base = 0
        for i in range(input_size):
            base += v[i] * (2 ** (input_size - i))
        prob_sum = 0.0
        for out in [0, 1]:
            idx = base + out
            prob_sum += abs(state[idx])**2
        key = format(K, '0{}b'.format(input_size))
        probs[key] = prob_sum
    return probs
