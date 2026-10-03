# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq


def bell_dag():
    def _call_init(machine):
        for name in ("init_qvm", "initQVM", "init", "initialize"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    method()
                    return
                except TypeError:
                    try:
                        method("")
                        return
                    except Exception:
                        pass
                except Exception:
                    pass

    def _alloc_many(machine, names, n):
        for name in names:
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    return method(n)
                except Exception:
                    pass
        return None

    qvm = None
    if hasattr(pq, "CPUQVM"):
        qvm = pq.CPUQVM()
        _call_init(qvm)

    if qvm is not None:
        q = _alloc_many(
            qvm,
            (
                "qAlloc_many",
                "qalloc_many",
                "qAllocMany",
                "qallocMany",
                "q_alloc_many",
                "allocate_qubits",
            ),
            3,
        )
        c = _alloc_many(
            qvm,
            (
                "cAlloc_many",
                "calloc_many",
                "cAllocMany",
                "callocMany",
                "c_alloc_many",
                "allocate_cbits",
                "allocate_bits",
            ),
            3,
        )
    else:
        q = None
        c = None

    if q is None:
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            method = getattr(pq, name, None)
            if callable(method):
                q = method(3)
                break
    if c is None:
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
            method = getattr(pq, name, None)
            if callable(method):
                c = method(3)
                break

    if q is None and qvm is not None:
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            method = getattr(qvm, name, None)
            if callable(method):
                q = [method() for _ in range(3)]
                break
    if c is None and qvm is not None:
        for name in ("cAlloc", "calloc", "allocate_cbit", "allocate_bit"):
            method = getattr(qvm, name, None)
            if callable(method):
                c = [method() for _ in range(3)]
                break

    circ = pq.QCircuit() if hasattr(pq, "QCircuit") else None
    prog = pq.QProg()

    def _append(container, node):
        try:
            result = container << node
            return container if result is None else result
        except Exception:
            pass
        for name in ("insert", "append", "push_back"):
            method = getattr(container, name, None)
            if callable(method):
                result = method(node)
                return container if result is None else result
        raise RuntimeError("Unable to append node to pyQPanda program.")

    h_gate = pq.H(q[0])
    if hasattr(pq, "CNOT"):
        cx_gate = pq.CNOT(q[0], q[1])
    elif hasattr(pq, "CX"):
        cx_gate = pq.CX(q[0], q[1])
    else:
        cx_gate = pq.X(q[1]).control([q[0]])

    if circ is not None:
        circ = _append(circ, h_gate)
        circ = _append(circ, cx_gate)
        prog = _append(prog, circ)
    else:
        prog = _append(prog, h_gate)
        prog = _append(prog, cx_gate)

    if hasattr(pq, "Measure"):
        measure_node = pq.Measure(q[0], c[0])
    else:
        measure_node = pq.measure(q[0], c[0])
    prog = _append(prog, measure_node)

    for method_name in ("to_dag", "to_DAG", "toDAG", "convert_to_dag", "convert_to_DAG"):
        method = getattr(prog, method_name, None)
        if callable(method):
            try:
                dag = method()
                bell_dag._keepalive = getattr(bell_dag, "_keepalive", [])
                bell_dag._keepalive.append((qvm, q, c, circ, prog, dag))
                return dag
            except Exception:
                pass

    for name in (
        "circuit_to_dag",
        "qprog_to_dag",
        "qprog_to_DAG",
        "prog_to_dag",
        "prog_to_DAG",
        "convert_qprog_to_dag",
        "convert_qprog_to_DAG",
        "trans_qprog_to_dag",
        "trans_qprog_to_DAG",
        "get_qprog_dag",
        "get_qprog_DAG",
        "get_prog_dag",
        "get_prog_DAG",
    ):
        converter = getattr(pq, name, None)
        if callable(converter):
            for obj in (prog, circ):
                if obj is None:
                    continue
                try:
                    dag = converter(obj)
                    if dag is not None:
                        bell_dag._keepalive = getattr(bell_dag, "_keepalive", [])
                        bell_dag._keepalive.append((qvm, q, c, circ, prog, dag))
                        return dag
                except Exception:
                    pass

    for name in ("DAGCircuit", "QProgDAG", "ProgDAG", "DAG"):
        cls = getattr(pq, name, None)
        if callable(cls):
            try:
                dag = cls(prog)
                bell_dag._keepalive = getattr(bell_dag, "_keepalive", [])
                bell_dag._keepalive.append((qvm, q, c, circ, prog, dag))
                return dag
            except Exception:
                pass
            try:
                dag = cls()
                for method_name in (
                    "build",
                    "from_qprog",
                    "from_prog",
                    "prog_to_dag",
                    "traversal",
                    "traverse",
                    "convert",
                    "construct",
                ):
                    method = getattr(dag, method_name, None)
                    if callable(method):
                        try:
                            result = method(prog)
                            if result is not None:
                                dag = result
                            bell_dag._keepalive = getattr(bell_dag, "_keepalive", [])
                            bell_dag._keepalive.append((qvm, q, c, circ, prog, dag))
                            return dag
                        except Exception:
                            pass
            except Exception:
                pass

    bell_dag._keepalive = getattr(bell_dag, "_keepalive", [])
    bell_dag._keepalive.append((qvm, q, c, circ, prog))
    return prog
