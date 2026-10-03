# EVAL_META: task_id=27, framework=qpanda, class=3
import pyqpanda3.core as pq


def apply_op_back():
    prog = pq.QProg()
    prog << pq.I(2)
    prog << pq.H(0)
    prog << pq.CNOT(0, 1)
    prog << pq.H(0)

    simulator = pq.CPUQVM()
    simulator.run(prog, 1)

    if hasattr(pq, "QProgDAG"):
        return pq.QProgDAG(prog)
    return prog
