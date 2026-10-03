# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, CNot

def bv_function(s):
    n = len(s)
    prog = QProg()
    qubits = [Qubit(i) for i in range(n + 1)]
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog.insert(CNot(qubits[index], qubits[n]))
    return prog
