# EVAL_META: task_id=52, framework=qpanda, class=1
import pyqpanda3.core as pq


def send_bits(bitstring):
    machine = pq.CPUQVM()
    init_method = (
        getattr(machine, "init_qvm", None)
        or getattr(machine, "init", None)
        or getattr(machine, "initQVM", None)
    )
    if init_method is not None:
        init_method()

    qalloc_many = (
        getattr(machine, "qAlloc_many", None)
        or getattr(machine, "qalloc_many", None)
        or getattr(machine, "qAllocMany", None)
    )
    calloc_many = (
        getattr(machine, "cAlloc_many", None)
        or getattr(machine, "calloc_many", None)
        or getattr(machine, "cAllocMany", None)
    )

    if qalloc_many is not None:
        qubits = qalloc_many(2)
    else:
        qalloc = getattr(machine, "qAlloc", None) or getattr(machine, "qalloc")
        qubits = [qalloc(), qalloc()]

    if calloc_many is not None:
        cbits = calloc_many(2)
    else:
        calloc = getattr(machine, "cAlloc", None) or getattr(machine, "calloc")
        cbits = [calloc(), calloc()]

    cnot_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    measure_gate = getattr(pq, "Measure", None) or getattr(pq, "measure")

    def add(prog, op):
        try:
            return prog << op
        except Exception:
            ret = prog.insert(op)
            return prog if ret is None else ret

    prog = pq.QProg()
    prog = add(prog, pq.H(qubits[0]))
    prog = add(prog, cnot_gate(qubits[0], qubits[1]))

    if bitstring[1] == "1":
        prog = add(prog, pq.Z(qubits[0]))
    if bitstring[0] == "1":
        prog = add(prog, pq.X(qubits[0]))

    prog = add(prog, cnot_gate(qubits[0], qubits[1]))
    prog = add(prog, pq.H(qubits[0]))
    prog = add(prog, measure_gate(qubits[0], cbits[0]))
    prog = add(prog, measure_gate(qubits[1], cbits[1]))

    if not hasattr(send_bits, "_machines"):
        send_bits._machines = []
    send_bits._machines.append(machine)

    return prog
