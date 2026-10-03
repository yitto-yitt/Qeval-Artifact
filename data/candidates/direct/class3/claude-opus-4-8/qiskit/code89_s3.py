# EVAL_META: task_id=89, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate


def create_controlled_hgate():
    qc = QuantumCircuit(3)
    ch = HGate().control(2)
    qc.append(ch, [0, 1, 2])
    return qc
