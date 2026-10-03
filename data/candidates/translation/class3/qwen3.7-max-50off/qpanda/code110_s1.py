# EVAL_META: task_id=110, framework=qpanda, class=3
import pyqpanda3.core as pq

def equivalent_clifford_circuit(circuit, n):
    res = []
    for _ in range(n):
        prog = pq.QProg()
        prog << circuit
        res.append(prog)
    return res
