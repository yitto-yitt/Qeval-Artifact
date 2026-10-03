# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np


def dj_algorithm(oracle):
    if isinstance(oracle, cirq.Circuit):
        oracle_circuit = oracle
        qubits = sorted(oracle_circuit.all_qubits())
    elif isinstance(oracle, cirq.Gate):
        nq = oracle.num_qubits() if callable(getattr(oracle, "num_qubits", None)) else oracle.num_qubits
        qubits = list(cirq.LineQubit.range(nq))
        oracle_circuit = cirq.Circuit(oracle.on(*qubits))
    elif isinstance(oracle, cirq.Operation):
        qubits = list(oracle.qubits)
        oracle_circuit = cirq.Circuit(oracle)
    else:
        oracle_circuit = cirq.Circuit(oracle)
        qubits = sorted(oracle_circuit.all_qubits())

    n = len(qubits)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(oracle_circuit)
    circuit.append(cirq.H.on_each(*qubits))

    result = cirq.Simulator().simulate(circuit, qubit_order=qubits)
    state = result.final_state_vector

    probs = {}
    for i, amp in enumerate(state):
        p = float(abs(amp) ** 2)
        if p > 1e-12:
            bits = cirq.big_endian_int_to_bits(i, bit_count=n)
            key = "".join(str(b) for b in reversed(bits[: n - 1]))
            probs[key] = probs.get(key, 0.0) + p

    return {k: v for k, v in probs.items() if not np.isclose(v, 0.0)}
