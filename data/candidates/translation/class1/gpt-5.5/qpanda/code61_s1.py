# EVAL_META: task_id=61, framework=qpanda, class=1
import pyqpanda3.core as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = pq.CPUQVM()

    for init_name in ("init_qvm", "init"):
        init = getattr(qvm, init_name, None)
        if init is not None:
            try:
                init()
            except TypeError:
                init("")
            break

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(1)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(1)
    elif hasattr(qvm, "allocate_qubits"):
        q = qvm.allocate_qubits(1)
    else:
        q = [qvm.qAlloc()]

    if hasattr(qvm, "cAlloc_many"):
        c = qvm.cAlloc_many(1)
    elif hasattr(qvm, "calloc_many"):
        c = qvm.calloc_many(1)
    elif hasattr(qvm, "allocate_cbits"):
        c = qvm.allocate_cbits(1)
    else:
        c = [qvm.cAlloc()]

    prog = pq.QProg()

    if hasattr(pq, "measure_all"):
        meas = pq.measure_all(q, c)
    elif hasattr(pq, "Measure"):
        meas = pq.Measure(q[0], c[0])
    else:
        meas = pq.measure(q[0], c[0])

    try:
        prog << meas
    except Exception:
        prog.insert(meas)

    if not hasattr(create_quantum_circuit_with_one_qubit_and_measure, "_qvms"):
        create_quantum_circuit_with_one_qubit_and_measure._qvms = []
    create_quantum_circuit_with_one_qubit_and_measure._qvms.append(qvm)

    return prog
