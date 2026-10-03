# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3 import core as pq


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "initQVM", "init"):
        init_func = getattr(machine, init_name, None)
        if init_func is not None:
            init_func()
            break

    qalloc_many = (
        getattr(machine, "qAlloc_many", None)
        or getattr(machine, "qalloc_many", None)
        or getattr(machine, "qAllocMany", None)
        or getattr(machine, "qallocMany", None)
    )
    calloc_many = (
        getattr(machine, "cAlloc_many", None)
        or getattr(machine, "calloc_many", None)
        or getattr(machine, "cAllocMany", None)
        or getattr(machine, "callocMany", None)
    )

    qubits = qalloc_many(2)
    cbits = calloc_many(2)

    prog = pq.QProg()

    def add(op):
        nonlocal prog
        prog = prog << op

    cnot_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    ry_gate = getattr(pq, "RY")
    measure_gate = getattr(pq, "Measure", None) or getattr(pq, "measure")

    add(pq.H(qubits[0]))
    add(cnot_gate(qubits[0], qubits[1]))

    barrier_gate = getattr(pq, "BARRIER", None) or getattr(pq, "Barrier", None)
    if barrier_gate is not None:
        try:
            add(barrier_gate(qubits))
        except TypeError:
            try:
                add(barrier_gate(qubits[0], qubits[1]))
            except TypeError:
                pass

    if alice == 0:
        add(ry_gate(qubits[0], 0))
    else:
        add(ry_gate(qubits[0], -pi / 2))

    add(measure_gate(qubits[0], cbits[0]))

    if bob == 0:
        add(ry_gate(qubits[1], -pi / 4))
    else:
        add(ry_gate(qubits[1], pi / 4))

    add(measure_gate(qubits[1], cbits[1]))

    if not hasattr(chsh_circuit, "_machines"):
        chsh_circuit._machines = []
    chsh_circuit._machines.append(machine)

    return prog
