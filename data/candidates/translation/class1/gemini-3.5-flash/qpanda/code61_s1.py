# EVAL_META: task_id=61, framework=qpanda, class=1
import pyqpanda3.core as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = pq.init_quantum_share()
    q = pq.qAlloc()
    c = pq.cAlloc()
    prog = pq.QProg()
    prog << pq.Measure(q, c)
    return prog
