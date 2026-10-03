# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import YGate


def mcy(qc):
    mcy_gate = YGate().control(4)
    qc.append(mcy_gate, [0, 1, 2, 3, 4])
    return qc
