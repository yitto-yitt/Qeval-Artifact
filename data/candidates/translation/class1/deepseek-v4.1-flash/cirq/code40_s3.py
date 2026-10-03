# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    psi = np.array(desired_vector, dtype=complex)
    psi = psi / np.linalg.norm(psi)
    dim = len(psi)
    e0 = np.zeros(dim, dtype=complex)
    e0[0] = 1.0
    v = e0 - psi
    v_norm_sq = np.vdot(v, v).real
    if v_norm_sq < 1e-12:
        U = np.eye(dim, dtype=complex)
    else:
        U = np.eye(dim, dtype=complex) - 2 * np.outer(v, np.conj(v)) / v_norm_sq
    qubits = [cirq.LineQubit(2), cirq.LineQubit(1), cirq.LineQubit(0)]
    circuit = cirq.Circuit()
    circuit.append(cirq.MatrixGate(U).on(*qubits))
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
