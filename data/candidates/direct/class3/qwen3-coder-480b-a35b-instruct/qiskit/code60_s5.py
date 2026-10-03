# EVAL_META: task_id=60, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import CXGate, SdgGate, SGate

def create_cy_gate():
    qc = QuantumCircuit(2)
    qc.append(SdgGate(), [1])
    qc.append(CXGate(), [0, 1])
    qc.append(SGate(), [1])
    return qc
