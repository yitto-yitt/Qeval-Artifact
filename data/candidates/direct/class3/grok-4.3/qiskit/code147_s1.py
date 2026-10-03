# EVAL_META: task_id=147, framework=qiskit, class=3
import math
def mcy(qc):
    qc.mcry(math.pi, [0, 1, 2, 3], 4)
