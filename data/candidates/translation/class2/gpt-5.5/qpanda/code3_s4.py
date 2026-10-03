# EVAL_META: task_id=3, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()

    for init_name in ("init_qvm", "init"):
        init_method = getattr(machine, init_name, None)
        if init_method is not None:
            try:
                init_method()
            except TypeError:
                pass
            break

    def _call_first(obj, names, *args):
        for name in names:
            method = getattr(obj, name, None)
            if method is not None:
                return method(*args)
        raise AttributeError(names[0])

    qubits = _call_first(
        machine,
        ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"),
        3,
    )
    cbits = _call_first(
        machine,
        ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany", "allocate_cbits"),
        3,
    )

    prog = pq.QProg()
    cnot = getattr(pq, "CNOT", getattr(pq, "CX", None))
    measure = getattr(pq, "Measure", getattr(pq, "measure", None))

    prog << pq.H(qubits[0])
    prog << cnot(qubits[0], qubits[1])
    prog << cnot(qubits[0], qubits[2])

    for i in range(3):
        prog << measure(qubits[i], cbits[i])

    if not hasattr(create_ghz, "_resources"):
        create_ghz._resources = []
    create_ghz._resources.append((machine, qubits, cbits))

    if drawing:
        return prog, str(prog)
    return prog
