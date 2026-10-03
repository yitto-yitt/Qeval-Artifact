# EVAL_META: task_id=52, framework=qpanda, class=1
import pyqpanda3.core as pq


def send_bits(bitstring):
    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(machine, init_name):
            try:
                getattr(machine, init_name)()
            except TypeError:
                pass
            break

    qalloc = (
        getattr(machine, "qAlloc_many", None)
        or getattr(machine, "qalloc_many", None)
        or getattr(machine, "qAllocMany", None)
    )
    calloc = (
        getattr(machine, "cAlloc_many", None)
        or getattr(machine, "calloc_many", None)
        or getattr(machine, "cAllocMany", None)
    )

    qubits = qalloc(2)
    cbits = calloc(2)

    cnot = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    measure = getattr(pq, "Measure", None) or getattr(pq, "measure")

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << cnot(qubits[0], qubits[1])

    if bitstring[1] == "1":
        prog << pq.Z(qubits[0])
    if bitstring[0] == "1":
        prog << pq.X(qubits[0])

    prog << cnot(qubits[0], qubits[1])
    prog << pq.H(qubits[0])
    prog << measure(qubits[0], cbits[0])
    prog << measure(qubits[1], cbits[1])

    if not hasattr(send_bits, "_machines"):
        send_bits._machines = []
    send_bits._machines.append(machine)

    return prog
