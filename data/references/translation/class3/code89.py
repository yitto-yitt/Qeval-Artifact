# EVAL_META: task_id=89, framework=qiskit, class=3

from qiskit.circuit.library import HGate
from qiskit import QuantumCircuit, QuantumRegister

def create_controlled_hgate():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    c3h_gate = HGate().control(2)
    qc.append(c3h_gate, qr)
    return qc


# ==================================================
