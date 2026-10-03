# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq


def bell_each_shot():
    shots = 10

    qvm_cls = None
    for name in ("CPUQVM", "CPUSingleThreadQVM"):
        if hasattr(pq, name):
            qvm_cls = getattr(pq, name)
            break
    qvm = qvm_cls()

    for init_name in ("init_qvm", "init", "initialize"):
        if hasattr(qvm, init_name):
            getattr(qvm, init_name)()
            break

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(2)
    else:
        qubits = qvm.qalloc_many(2)

    if hasattr(qvm, "cAlloc_many"):
        cbits = qvm.cAlloc_many(2)
    else:
        cbits = qvm.calloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])

    if hasattr(pq, "Measure"):
        prog << pq.Measure(qubits[0], cbits[0])
        prog << pq.Measure(qubits[1], cbits[1])
    elif hasattr(pq, "measure_all"):
        prog << pq.measure_all(qubits, cbits)
    else:
        prog << pq.MeasureAll(qubits, cbits)

    if hasattr(qvm, "run_with_configuration"):
        counts = qvm.run_with_configuration(prog, cbits, shots)
    else:
        counts = pq.run_with_configuration(prog, cbits, shots)

    normalized_counts = {}
    if isinstance(counts, dict):
        items = counts.items()
    else:
        tmp = {}
        for outcome in counts:
            tmp[outcome] = tmp.get(outcome, 0) + 1
        items = tmp.items()

    for key, value in items:
        if isinstance(key, int):
            bitstring = format(key, "02b")
        elif isinstance(key, (list, tuple)):
            bitstring = "".join(str(int(x)) for x in key)
        else:
            bitstring = str(key).replace(" ", "")
            if bitstring.startswith("0b"):
                bitstring = bitstring[2:]
            bitstring = bitstring.zfill(2)
        normalized_counts[bitstring] = normalized_counts.get(bitstring, 0) + value

    total = sum(normalized_counts.values())
    result = {key: value / total for key, value in normalized_counts.items()}

    for finalize_name in ("finalize", "finalize_qvm"):
        if hasattr(qvm, finalize_name):
            getattr(qvm, finalize_name)()
            break

    return result
