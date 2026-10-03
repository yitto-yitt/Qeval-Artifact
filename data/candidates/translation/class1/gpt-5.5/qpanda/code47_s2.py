# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    shots = int(samples)

    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(1)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(1)
    else:
        qubits = [0]

    if hasattr(qvm, "cAlloc_many"):
        cbits = qvm.cAlloc_many(1)
    elif hasattr(qvm, "calloc_many"):
        cbits = qvm.calloc_many(1)
    else:
        cbits = [0]

    try:
        prog = pq.QProg()
    except TypeError:
        prog = pq.QProg(1)

    prog << pq.H(qubits[0])

    if hasattr(pq, "Measure"):
        prog << pq.Measure(qubits[0], cbits[0])
    elif hasattr(pq, "measure"):
        prog << pq.measure(qubits[0], cbits[0])
    else:
        prog << pq.measure_all(qubits, cbits)

    if hasattr(qvm, "run_with_configuration"):
        try:
            result = qvm.run_with_configuration(prog, cbits, shots)
        except TypeError:
            result = qvm.run_with_configuration(prog, shots)
    else:
        result = qvm.run(prog, shots)

    counts = result.get_counts() if hasattr(result, "get_counts") else result

    heads = 0.0
    tails = 0.0
    for key, value in counts.items():
        bit = str(key).strip()
        val = float(value)
        if bit in ("0", "False", "false"):
            heads += val
        elif bit in ("1", "True", "true"):
            tails += val
        else:
            bits = [ch for ch in bit if ch in "01"]
            if bits:
                if bits[-1] == "0":
                    heads += val
                else:
                    tails += val

    if hasattr(qvm, "finalize"):
        qvm.finalize()

    total = heads + tails
    return {"Heads": heads / total, "Tails": tails / total}
