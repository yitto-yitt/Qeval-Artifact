# EVAL_META: task_id=61, framework=qpanda2, class=1
import pyqpanda as pq

_QVM = None


def create_quantum_circuit_with_one_qubit_and_measure():
    global _QVM
    if _QVM is None:
        _QVM = pq.CPUQVM()
        _QVM.init_qvm()

    q = _QVM.qAlloc_many(1)
    c = _QVM.cAlloc_many(1)

    prog = pq.QProg()
    prog << pq.Measure(q[0], c[0])

    return prog
