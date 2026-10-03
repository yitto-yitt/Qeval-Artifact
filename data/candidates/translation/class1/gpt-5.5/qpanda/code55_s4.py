# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq

def or_gate(a, b):
    qvm = pq.CPUQVM()
    for _name in ("init_qvm", "init"):
        _method = getattr(qvm, _name, None)
        if callable(_method):
            _method()
            break

    qalloc = getattr(qvm, "qAlloc_many", None) or getattr(qvm, "qalloc_many", None) or getattr(qvm, "allocate_qubits", None)
    calloc = getattr(qvm, "cAlloc_many", None) or getattr(qvm, "calloc_many", None) or getattr(qvm, "allocate_cbits", None)

    qr_a = qalloc(3)
    qr_b = qalloc(3)
    ancillary = qalloc(3)
    measure = calloc(3) if callable(calloc) else None

    prog = pq.QProg()

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "0":
            prog << pq.X(qr_a[i])
        if b_bits[2 - i] == "0":
            prog << pq.X(qr_b[i])

    toffoli = getattr(pq, "Toffoli", None)
    for i in range(3):
        if callable(toffoli):
            prog << toffoli(qr_a[i], qr_b[i], ancillary[i])
        else:
            prog << pq.X(ancillary[i]).control([qr_a[i], qr_b[i]])

    for i in range(3):
        prog << pq.X(ancillary[i])

    probs = None
    prob_run = getattr(qvm, "prob_run_dict", None)
    if callable(prob_run):
        probs = prob_run(prog, [ancillary[2], ancillary[1], ancillary[0]], -1)

    if probs is None:
        if measure is not None:
            measure_gate = getattr(pq, "Measure", None)
            if callable(measure_gate):
                for i in range(3):
                    prog << measure_gate(ancillary[i], measure[i])
            else:
                prog << pq.measure_all(ancillary, measure)

            run_cfg = getattr(qvm, "run_with_configuration", None)
            if callable(run_cfg):
                counts = run_cfg(prog, measure, 1024)
            else:
                result = qvm.run(prog, measure, 1024)
                counts = result.get_counts() if hasattr(result, "get_counts") else result
            total = sum(counts.values())
            return {str(k)[-3:].zfill(3): v / total for k, v in counts.items() if v}
        raise RuntimeError("No supported pyQPanda3 execution method found")

    result = {}
    for key, value in probs.items():
        value = float(value)
        if value > 1e-12:
            if isinstance(key, int):
                bitstr = format(key, "03b")
            else:
                bitstr = "".join(ch for ch in str(key) if ch in "01")
                bitstr = bitstr[-3:].zfill(3)
            result[bitstr] = value

    total = sum(result.values())
    if total != 0:
        result = {k: v / total for k, v in result.items()}
    return result
