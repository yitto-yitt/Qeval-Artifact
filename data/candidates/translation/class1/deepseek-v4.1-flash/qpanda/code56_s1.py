# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq

def not_gate(a):
    a_str = format(a, "08b")
    qvm = pq.CPUQVM()
    if hasattr(qvm, 'init_qvm'):
        qvm.init_qvm()
    
    Measure = getattr(pq, 'Measure', getattr(pq, 'measure', None))
    if Measure is None:
        raise ImportError("No Measure function found in pyqpanda3.core")
    
    def build_prog(use_objects=False):
        prog = pq.QProg()
        if use_objects:
            q = qvm.qAlloc_many(8)
            c = qvm.cAlloc_many(8)
            for i in range(8):
                if a_str[7 - i] == "0":
                    prog << pq.X(q[i])
            for i in range(8):
                prog << Measure(q[i], c[i])
            return prog, q, c
        else:
            for i in range(8):
                if a_str[7 - i] == "0":
                    prog << pq.X(i)
            for i in range(8):
                prog << Measure(i, i)
            return prog, None, None

    try:
        prog, q, c = build_prog(False)
        ret = qvm.run(prog, 1024)
    except Exception:
        prog, q, c = build_prog(True)
        if hasattr(qvm, 'run'):
            try:
                ret = qvm.run(prog, 1024)
            except Exception:
                ret = qvm.run_with_configuration(prog, c, 1024)
        else:
            ret = qvm.run_with_configuration(prog, c, 1024)

    counts = None
    if hasattr(ret, 'get_counts'):
        counts = ret.get_counts()
    else:
        if hasattr(qvm, 'get_result'):
            counts = qvm.get_result().get_counts()
        elif hasattr(qvm, 'result'):
            counts = qvm.result().get_counts()
        else:
            raise RuntimeError("Cannot get counts")

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
