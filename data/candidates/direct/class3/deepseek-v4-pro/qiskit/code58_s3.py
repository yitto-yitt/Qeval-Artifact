# EVAL_META: task_id=58, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate, CXGate

def create_ch_gate():
    qc = QuantumCircuit(2, name="CH")
    qc.append(RYGate(math.pi / 4), [1])
    qc.append(CXGate(), [0, 1])
    qc.append(RYGate(-math.pi / 4), [1])
    return qc
