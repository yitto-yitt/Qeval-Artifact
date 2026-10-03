# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        qc = QuantumCircuit(1, 1)
        qc.measure(0, 0)
        return qc
    keys = list(probability_dist.keys())
    n = len(keys[0])
    dim = 2 ** n
    state = []
    for i in range(dim):
        bitstr = f"{i:0{n}b}"
        p = probability_dist.get(bitstr, 0.0)
        state.append(math.sqrt(max(p, 0.0)))
    qc = QuantumCircuit(n, n)
    qc.append(StatePreparation(state), range(n))
    qc.measure(range(n), range(n))
    return qc
