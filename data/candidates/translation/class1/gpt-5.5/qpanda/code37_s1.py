# EVAL_META: task_id=37, framework=qpanda, class=1
import pyqpanda3.core as pq


def bv_algorithm(s):
    n = len(s)

    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()

    qalloc = (
        getattr(machine, "qAlloc_many", None)
        or getattr(machine, "qalloc_many", None)
        or getattr(machine, "qAllocMany", None)
        or getattr(machine, "allocate_qubits", None)
    )
    calloc = (
        getattr(machine, "cAlloc_many", None)
        or getattr(machine, "calloc_many", None)
        or getattr(machine, "cAllocMany", None)
        or getattr(machine, "allocate_cbits", None)
    )

    q = qalloc(n + 1)
    c = calloc(n)

    prog = pq.QProg()

    h_gate = getattr(pq, "H")
    x_gate = getattr(pq, "X")
    cx_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    measure_gate = getattr(pq, "Measure", None) or getattr(pq, "measure")

    ancilla = n

    prog << x_gate(q[ancilla])
    for i in range(n + 1):
        prog << h_gate(q[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << cx_gate(q[index], q[ancilla])

    for i in range(n):
        prog << h_gate(q[i])

    for i in range(n):
        prog << measure_gate(q[n - 1 - i], c[i])

    if hasattr(machine, "run_with_configuration"):
        try:
            result = machine.run_with_configuration(prog, c, 1)
        except TypeError:
            result = machine.run_with_configuration(prog, 1)
    elif hasattr(machine, "run"):
        try:
            result = machine.run(prog, c, 1)
        except TypeError:
            result = machine.run(prog, 1)
    else:
        result = machine.prob_run_dict(prog, q[:n], 1)

    if isinstance(result, dict):
        bitstring = max(result.items(), key=lambda item: item[1])[0] if result else ""
    elif hasattr(result, "get_counts"):
        counts = result.get_counts()
        bitstring = max(counts.items(), key=lambda item: item[1])[0] if counts else ""
    elif hasattr(result, "items"):
        counts = dict(result.items())
        bitstring = max(counts.items(), key=lambda item: item[1])[0] if counts else ""
    else:
        bitstring = str(result)

    bitstrings = [bitstring]
    return [bitstrings, result]
