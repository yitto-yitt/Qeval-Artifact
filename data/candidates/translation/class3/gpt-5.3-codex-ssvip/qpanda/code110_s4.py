# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import Clifford


def equivalent_clifford_circuit(circuit, n):
    target = circuit if isinstance(circuit, Clifford) else Clifford(circuit)
    num_qubits = target.num_qubits
    result = []
    while len(result) < n:
        cand = Clifford.random(num_qubits)
        if np.allclose(cand.matrix(), target.matrix(), rtol=0.4, atol=0.4):
            result.append(cand)
    return result
