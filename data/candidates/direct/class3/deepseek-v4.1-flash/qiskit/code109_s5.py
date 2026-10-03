# EVAL_META: task_id=109, framework=qiskit, class=3
import numpy as np
from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.circuit.library import UGate

def circuit():
    phi = Parameter('phi')
    qc = QuantumCircuit(1)
    qc.append(UGate(np.pi/2, phi, 0), [0])
    return qc
