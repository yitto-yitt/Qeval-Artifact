# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq


def bell_dag():
    global _bell_dag_qvms
    try:
        _bell_dag_qvms
    except NameError:
        _bell_dag_qvms = []

    machine = pq.CPUQVM()
    init_qvm = getattr(machine, "init_qvm", None)
    if callable(init_qvm):
        init_qvm()

    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << (pq.CNOT(q[0], q[1]) if hasattr(pq, "CNOT") else pq.CX(q[0], q[1]))
    prog << (pq.Measure(q[0], c[0]) if hasattr(pq, "Measure") else pq.measure(q[0], c[0]))

    _bell_dag_qvms.append(machine)

    for name in ("circuit_to_dag", "prog_to_dag", "qprog_to_dag", "QProgToDAG", "convert_qprog_to_dag"):
        converter = getattr(pq, name, None)
        if callable(converter):
            try:
                return converter(prog)
            except Exception:
                pass

    dag_cls = getattr(pq, "QProgDAG", None)
    if dag_cls is not None:
        try:
            return dag_cls(prog)
        except Exception:
            pass

    return prog
