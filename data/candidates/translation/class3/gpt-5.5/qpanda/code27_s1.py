# EVAL_META: task_id=27, framework=qpanda, class=3
import pyqpanda3.core as pq


def apply_op_back():
    machine = pq.CPUQVM()

    for init_name in ("init_qvm", "init", "initialize"):
        init_func = getattr(machine, init_name, None)
        if init_func is not None:
            try:
                init_func()
                break
            except TypeError:
                pass

    q = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "qAllocMany"):
        alloc_func = getattr(machine, alloc_name, None)
        if alloc_func is not None:
            q = alloc_func(3)
            break

    for calloc_name in ("cAlloc_many", "calloc_many", "allocate_cbits", "cAllocMany"):
        calloc_func = getattr(machine, calloc_name, None)
        if calloc_func is not None:
            try:
                calloc_func(3)
                break
            except Exception:
                pass

    prog = pq.QProg()

    h_gate = getattr(pq, "H")
    cx_gate = getattr(pq, "CNOT", None)
    if cx_gate is None:
        cx_gate = getattr(pq, "CX")

    for gate in (h_gate(q[0]), cx_gate(q[0], q[1]), h_gate(q[0])):
        try:
            new_prog = prog << gate
            if new_prog is not None:
                prog = new_prog
        except Exception:
            prog.insert(gate)

    if not hasattr(apply_op_back, "_machines"):
        apply_op_back._machines = []
    apply_op_back._machines.append(machine)

    return prog
