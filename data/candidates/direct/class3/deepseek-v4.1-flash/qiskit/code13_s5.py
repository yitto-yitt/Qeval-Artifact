# EVAL_META: task_id=13, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate

def custom_rotation_gate():
    qc = QuantumCircuit(1)
    qc.append(UGate(pi / 2, pi / 2, pi / 2), [0])
    return qc
