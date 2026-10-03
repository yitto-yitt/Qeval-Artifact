# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import *


def send_bits(bitstring):
    try:
        qvm = CPUQVM()
    except NameError:
        qvm = init_quantum_machine(QMachineType.CPU)

    for init_name in ("init_qvm", "init", "initQVM"):
        init_method = getattr(qvm, init_name, None)
        if callable(init_method):
            init_method()
            break

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(2)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(2)
    else:
        q = qAlloc_many(2)

    if hasattr(qvm, "cAlloc_many"):
        c = qvm.cAlloc_many(2)
    elif hasattr(qvm, "calloc_many"):
        c = qvm.calloc_many(2)
    else:
        c = cAlloc_many(2)

    prog = QProg()

    cnot_gate = globals().get("CNOT", globals().get("CX"))
    measure_gate = globals().get("Measure", globals().get("measure"))

    def add(op):
        nonlocal prog
        try:
            result = prog << op
            if result is not None:
                prog = result
        except Exception:
            result = prog.insert(op)
            if result is not None:
                prog = result

    add(H(q[0]))
    add(cnot_gate(q[0], q[1]))

    if bitstring[1] == "1":
        add(Z(q[0]))
    if bitstring[0] == "1":
        add(X(q[0]))

    add(cnot_gate(q[0], q[1]))
    add(H(q[0]))
    add(measure_gate(q[0], c[0]))
    add(measure_gate(q[1], c[1]))

    if not hasattr(send_bits, "_machines"):
        send_bits._machines = []
    send_bits._machines.append(qvm)

    return prog
