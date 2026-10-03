# EVAL_META: task_id=61, framework=qpanda, class=1
import pyqpanda3 as qp

def create_quantum_circuit_with_one_qubit_and_measure():
    q = qp.Qubit()
    c = qp.CBit()
    prog = qp.QProg()
    prog << qp.Measure(q, c)
    return prog
