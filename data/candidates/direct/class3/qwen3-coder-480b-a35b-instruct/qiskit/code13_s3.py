# EVAL_META: task_id=13, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate
import math

def custom_rotation_gate():
    qc = QuantumCircuit(1)
    theta = math.pi / 2
    phi = math.pi / 2
    lam = math.pi / 2
    qc.append(UGate(theta, phi, lam), [0])
    return qc
