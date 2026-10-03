# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit.circuit.library import YGate

def mcy(qc):
    gate = YGate().control(4)
    qc.append(gate, [0, 1, 2, 3, 4])
    return qc
