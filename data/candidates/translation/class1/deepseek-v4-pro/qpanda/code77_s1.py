# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import QCircuit, StatePreparation, AllocateQubits

def circuit_from_probability_dist(probability_dist):
    max_key = max(probability_dist.keys()) if probability_dist else 0
    num_qubits = math.ceil(math.log2(max_key + 1)) or 1
    dim = 1 << num_qubits
    amplitudes = [math.sqrt(probability_dist.get(i, 0.0)) for i in range(dim)]

    qvec = AllocateQubits(num_qubits)
    circuit = QCircuit()
    sp = StatePreparation(qvec, amplitudes)
    circuit << sp
    return circuit
