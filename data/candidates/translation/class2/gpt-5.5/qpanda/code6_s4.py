# EVAL_META: task_id=6, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_state_prep(num_qubits):
    num_qubits = int(num_qubits)

    qvm_cls = (
        getattr(pq, "CPUQVM", None)
        or getattr(pq, "CPUSingleThreadQVM", None)
        or getattr(pq, "QVM", None)
    )
    qvm = qvm_cls()

    for init_name in ("init_qvm", "initQVM", "init", "initialize"):
        init = getattr(qvm, init_name, None)
        if init is not None:
            try:
                init()
            except TypeError:
                pass
            break

    alloc_many = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"):
        alloc_many = getattr(qvm, name, None)
        if alloc_many is not None:
            break

    if alloc_many is not None:
        qubits = list(alloc_many(num_qubits))
    else:
        alloc_one = None
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            alloc_one = getattr(qvm, name, None)
            if alloc_one is not None:
                break
        qubits = [alloc_one() for _ in range(num_qubits)]

    prog = pq.QProg()

    def add_gate(container, gate):
        try:
            result = container << gate
            return result if result is not None else container
        except Exception:
            result = container.insert(gate)
            return result if result is not None else container

    if num_qubits > 0:
        prog = add_gate(prog, pq.X(qubits[0]))

        identity_gate = getattr(pq, "I", None)
        for i in range(1, num_qubits):
            if identity_gate is not None:
                prog = add_gate(prog, identity_gate(qubits[i]))
            else:
                prog = add_gate(prog, pq.H(qubits[i]))
                prog = add_gate(prog, pq.H(qubits[i]))

    globals().setdefault("_QPANDA3_STATE_PREP_RESOURCES", []).append((qvm, qubits))
    return prog
