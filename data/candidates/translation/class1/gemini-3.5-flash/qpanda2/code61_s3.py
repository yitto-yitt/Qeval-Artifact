# EVAL_META: task_id=61, framework=qpanda2, class=1
import pyqpanda as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    try:
        q = pq.qAlloc()
        c = pq.cAlloc()
    except Exception:
        pq.init_quantum_machine(pq.QMachineType.CPU)
        q = pq.qAlloc()
        c = pq.cAlloc()

    prog = pq.QProg()
    prog << pq.Measure(q, c)
    return prog
