# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import *


def create_ghz(drawing=False):
    qvm = CPUQVM()
    init = getattr(qvm, "init_qvm", None)
    if init is None:
        init = getattr(qvm, "init", None)
    if init is not None:
        init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(3)
    else:
        qubits = [qvm.qAlloc() for _ in range(3)]

    if hasattr(qvm, "cAlloc_many"):
        cbits = qvm.cAlloc_many(3)
    else:
        cbits = [qvm.cAlloc() for _ in range(3)]

    prog = QProg()

    def append_node(node):
        try:
            prog.insert(node)
        except Exception:
            prog << node

    append_node(H(qubits[0]))

    cnot_gate = globals().get("CNOT", globals().get("CX"))
    append_node(cnot_gate(qubits[0], qubits[1]))
    append_node(cnot_gate(qubits[0], qubits[2]))

    measure_gate = globals().get("Measure", globals().get("measure"))
    if measure_gate is not None:
        for i in range(3):
            append_node(measure_gate(qubits[i], cbits[i]))
    else:
        append_node(measure_all(qubits, cbits))

    if not hasattr(create_ghz, "_qpanda_resources"):
        create_ghz._qpanda_resources = []
    create_ghz._qpanda_resources.append((qvm, qubits, cbits))

    if drawing:
        drawing_obj = str(prog)
        drawer = globals().get("draw_qprog")
        if drawer is not None:
            try:
                candidate = drawer(prog, "text")
                if candidate is not None:
                    drawing_obj = candidate
            except Exception:
                try:
                    candidate = drawer(prog)
                    if candidate is not None:
                        drawing_obj = candidate
                except Exception:
                    pass
        return prog, drawing_obj

    return prog
