# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit.circuit.library import YGate
def mcy(qc):
    qc.append(YGate().control(4), [0, 1, 2, 3, 4])
    return qc
