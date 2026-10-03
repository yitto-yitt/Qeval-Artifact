# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import *


def create_ghz(drawing=False):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(3)
    else:
        q = qvm.qalloc_many(3)

    if hasattr(qvm, "cAlloc_many"):
        c = qvm.cAlloc_many(3)
    else:
        c = qvm.calloc_many(3)

    prog = QProg()
    cnot_gate = globals().get("CNOT", globals().get("CX"))

    prog << H(q[0])
    prog << cnot_gate(q[0], q[1])
    prog << cnot_gate(q[0], q[2])

    measured = False
    measure_all_func = globals().get("measure_all")
    if callable(measure_all_func):
        try:
            prog << measure_all_func(q, c)
            measured = True
        except Exception:
            measured = False

    if not measured:
        measure_func = globals().get("Measure", globals().get("measure"))
        for i in range(3):
            prog << measure_func(q[i], c[i])

    if not hasattr(create_ghz, "_machines"):
        create_ghz._machines = []
    create_ghz._machines.append(qvm)

    if drawing:
        drawing_obj = None
        for name in ("draw_qprog", "draw_qprog_text", "circuit_draw", "draw"):
            draw_func = globals().get(name)
            if callable(draw_func):
                for args in ((prog,), (prog, "text"), (prog, "mpl")):
                    try:
                        drawing_obj = draw_func(*args)
                        break
                    except Exception:
                        pass
                if drawing_obj is not None:
                    break
        if drawing_obj is None:
            drawing_obj = str(prog)
        return prog, drawing_obj

    return prog
