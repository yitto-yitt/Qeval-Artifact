# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = len(oracle.qubits)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[n-1]))
    circuit.append(cirq.H.on_each(qubits))
    sorted_oracle_qubits = sorted(oracle.qubits, key=lambda q: getattr(q, 'x', str(q)))
    qubit_map = {old: new for old, new in zip(sorted_oracle_qubits, qubits)}
    mapped_oracle = oracle.transform_qubits(lambda q: qubit_map.get(q, q))
    circuit.append(mapped_oracle)
    circuit.append(cirq.H.on_each(qubits))
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    state = result.final_state_vector
    dim = 2 ** (n - 1)
    probs = np.abs(state).reshape((dim, 2)) ** 2
    probs = probs.sum(axis=1)
    dist = {}
    for i in range(dim):
        bs = format(i, f'0{n-1}b')[::-1]
        dist[bs] = float(probs[i])
    return {k: v for k, v in dist.items() if v > 1e-8}
