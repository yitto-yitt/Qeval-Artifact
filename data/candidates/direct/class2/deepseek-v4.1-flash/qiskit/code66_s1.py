# EVAL_META: task_id=66, framework=qiskit, class=2
import math
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    amp = 1 / math.sqrt(3)
    state = [0.0] * 8
    state[1] = amp
    state[2] = amp
    state[4] = amp
    qc.initialize(state, qc.qubits)
    qc.measure(qc.qubits, qc.clbits)
    return qc
