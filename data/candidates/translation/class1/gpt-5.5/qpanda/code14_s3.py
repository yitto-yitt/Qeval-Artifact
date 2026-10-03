# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq

def bell_each_shot():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    q_alloc = getattr(machine, "qAlloc_many", None) or getattr(machine, "qalloc_many", None)
    c_alloc = getattr(machine, "cAlloc_many", None) or getattr(machine, "calloc_many", None)
    q = q_alloc(2)
    c = c_alloc(2)

    prog = pq.QProg()
    cnot = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    prog << pq.H(q[0])
    prog << cnot(q[0], q[1])

    if hasattr(pq, "measure_all"):
        prog << pq.measure_all(q, c)
    else:
        measure = getattr(pq, "Measure")
        prog << measure(q[0], c[0])
        prog << measure(q[1], c[1])

    if hasattr(machine, "run_with_configuration"):
        try:
            counts = machine.run_with_configuration(prog, c, 10)
        except TypeError:
            counts = machine.run_with_configuration(prog, 10, c)
    else:
        counts = machine.run(prog, c, 10)

    if hasattr(counts, "get_counts"):
        counts = counts.get_counts()
    elif hasattr(counts, "counts"):
        counts = counts.counts

    normalized_counts = {}
    for key, value in dict(counts).items():
        if isinstance(key, str):
            bitstring = key.replace(" ", "")
        elif isinstance(key, (list, tuple)):
            bitstring = "".join(str(int(bit)) for bit in key)
        else:
            bitstring = str(key)
        normalized_counts[bitstring] = normalized_counts.get(bitstring, 0) + int(value)

    total = sum(normalized_counts.values())
    return {key: value / total for key, value in normalized_counts.items()}
