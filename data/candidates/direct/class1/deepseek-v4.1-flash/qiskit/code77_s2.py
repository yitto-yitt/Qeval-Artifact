# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit()
    
    keys = list(probability_dist.keys())
    
    if all(isinstance(k, str) for k in keys):
        n = max(len(k) for k in keys)
        index_prob = {int(k, 2): p for k, p in probability_dist.items()}
    elif all(isinstance(k, int) for k in keys):
        max_key = max(keys)
        n = max(1, max_key.bit_length())
        index_prob = dict(probability_dist)
    else:
        n = max(len(str(k)) for k in keys)
        index_prob = {int(str(k), 2): p for k, p in probability_dist.items()}
    
    total = sum(index_prob.values())
    state = [0.0] * (1 << n)
    for idx, p in index_prob.items():
        if 0 <= idx < len(state):
            state[idx] = math.sqrt(p / total)
    
    qc = QuantumCircuit(n)
    qc.append(StatePreparation(state), qc.qubits)
    qc.measure_all()
    return qc
