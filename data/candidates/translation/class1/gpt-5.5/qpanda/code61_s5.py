# EVAL_META: task_id=61, framework=qpanda, class=1
import pyqpanda3.core as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = pq.CPUQVM()

    for init_name in ("init_qvm", "init", "initQVM"):
        if hasattr(qvm, init_name):
            getattr(qvm, init_name)()
            break

    q_alloc = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        if hasattr(qvm, name):
            q_alloc = getattr(qvm, name)
            break

    c_alloc = None
    for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
        if hasattr(qvm, name):
            c_alloc = getattr(qvm, name)
            break

    q = q_alloc(1)
    c = c_alloc(1)

    prog = pq.QProg()
    measure = getattr(pq, "Measure", None) or getattr(pq, "measure")
    prog << measure(q[0], c[0])

    if not hasattr(create_quantum_circuit_with_one_qubit_and_measure, "_keepalive"):
        create_quantum_circuit_with_one_qubit_and_measure._keepalive = []
    create_quantum_circuit_with_one_qubit_and_measure._keepalive.append(qvm)

    return prog
