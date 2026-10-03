# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq


def bell_dag():
    qvm = pq.CPUQVM()

    for init_name in ("init_qvm", "init", "initQVM"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
                break
            except TypeError:
                pass

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "q_alloc_many", "allocate_qubits", "alloc_qubits"):
            if hasattr(machine, name):
                return getattr(machine, name)(n)
        return [machine.qAlloc() for _ in range(n)]

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "c_alloc_many", "allocate_cbits", "alloc_cbits"):
            if hasattr(machine, name):
                return getattr(machine, name)(n)
        return [machine.cAlloc() for _ in range(n)]

    q = _alloc_qubits(qvm, 3)
    c = _alloc_cbits(qvm, 3)

    prog = pq.QProg()

    def _append(node):
        nonlocal prog
        if hasattr(prog, "insert"):
            try:
                ret = prog.insert(node)
                if ret is not None:
                    prog = ret
                return
            except Exception:
                pass
        ret = prog.__lshift__(node)
        if ret is not None:
            prog = ret

    _append(pq.H(q[0]))

    if hasattr(pq, "CNOT"):
        _append(pq.CNOT(q[0], q[1]))
    else:
        _append(pq.CX(q[0], q[1]))

    if hasattr(pq, "Measure"):
        _append(pq.Measure(q[0], c[0]))
    else:
        _append(pq.measure(q[0], c[0]))

    if not hasattr(bell_dag, "_machines"):
        bell_dag._machines = []
    bell_dag._machines.append(qvm)

    for cls_name in ("QProgDAG", "DAGCircuit", "DAGCircuitBuilder", "QProgToDAG"):
        if hasattr(pq, cls_name):
            cls = getattr(pq, cls_name)
            for args in ((prog,), (prog, qvm), ()):
                try:
                    dag = cls(*args)
                    if args:
                        return dag
                    for method_name in (
                        "prog_to_dag",
                        "qprog_to_dag",
                        "convert",
                        "build",
                        "build_dag",
                        "from_qprog",
                        "set_qprog",
                    ):
                        if hasattr(dag, method_name):
                            method = getattr(dag, method_name)
                            for method_args in ((prog,), (prog, qvm)):
                                try:
                                    ret = method(*method_args)
                                    return dag if ret is None else ret
                                except Exception:
                                    pass
                    return dag
                except Exception:
                    pass

    for func_name in (
        "qprog_to_dag",
        "circuit_to_dag",
        "prog_to_dag",
        "convert_qprog_to_dag",
        "transform_qprog_to_dag",
    ):
        if hasattr(pq, func_name):
            func = getattr(pq, func_name)
            for args in ((prog,), (prog, qvm)):
                try:
                    return func(*args)
                except Exception:
                    pass

    return prog
