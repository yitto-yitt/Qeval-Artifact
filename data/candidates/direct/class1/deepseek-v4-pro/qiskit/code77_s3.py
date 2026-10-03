# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation


def circuit_from_probability_dist(probability_dist):
    keys = list(probability_dist.keys())
    if not keys:
        return QuantumCircuit(0)

    if isinstance(keys[0], int):
        n = max(k.bit_length() for k in keys)
        amplitudes = np.zeros(2**n, dtype=complex)
        for state, prob in probability_dist.items():
            amplitudes[state] = np.sqrt(prob)
    else:
        bitstrings = [str(k) for k in keys]
        n = max(len(b) for b in bitstrings)
        amplitudes = np.zeros(2**n, dtype=complex)
        for state, prob in probability_dist.items():
            bitstring = str(state)
            index = int(bitstring, 2)
            amplitudes[index] = np.sqrt(prob)

    qc = QuantumCircuit(n)
    qc.append(StatePreparation(amplitudes), qc.qubits)
    qc.measure_all()
    return qc
