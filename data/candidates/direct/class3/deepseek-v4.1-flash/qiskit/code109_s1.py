# EVAL_META: task_id=109, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.circuit.library import UGate
from math import pi

def circuit():
    phi = Parameter('phi')
    qc = QuantumCircuit(1)
    qc.append(UGate(pi/2, phi, 0), [0])
    return qc
