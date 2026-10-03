# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    samples = int(samples)

    def _try_methods(obj, names, *args, **kwargs):
        last_exc = None
        for name in names:
            if hasattr(obj, name):
                try:
                    return getattr(obj, name)(*args, **kwargs)
                except TypeError as exc:
                    last_exc = exc
                    continue
        if last_exc is not None:
            raise last_exc
        raise AttributeError(names[0])

    qvm = pq.CPUQVM()

    for init_name in ("init_qvm", "init"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
                break
            except TypeError:
                pass

    qubits = _try_methods(qvm, ("qAlloc_many", "qalloc_many", "qAllocMany", "qalloc_many"), 1)
    cbits = _try_methods(qvm, ("cAlloc_many", "calloc_many", "cAllocMany", "calloc_many"), 1)

    prog = pq.QProg()
    prog << pq.H(qubits[0])

    measured = False
    for meas_name in ("measure_all", "MeasureAll"):
        if hasattr(pq, meas_name):
            try:
                prog << getattr(pq, meas_name)(qubits, cbits)
                measured = True
                break
            except TypeError:
                pass

    if not measured:
        for meas_name in ("Measure", "measure"):
            if hasattr(pq, meas_name):
                prog << getattr(pq, meas_name)(qubits[0], cbits[0])
                measured = True
                break

    result = None
    run_attempts = (
        ("run_with_configuration", (prog, cbits, samples), {}),
        ("run_with_configuration", (prog, cbits), {"shots": samples}),
        ("run_with_config", (prog, cbits, samples), {}),
        ("run_with_config", (prog, cbits), {"shots": samples}),
        ("run", (prog, cbits, samples), {}),
        ("run", (prog,), {"shots": samples}),
    )

    last_exc = None
    for name, args, kwargs in run_attempts:
        if hasattr(qvm, name):
            try:
                result = getattr(qvm, name)(*args, **kwargs)
                break
            except TypeError as exc:
                last_exc = exc
                continue

    if result is None:
        if last_exc is not None:
            raise last_exc
        raise AttributeError("No compatible run method found")

    if hasattr(result, "get_counts"):
        counts = result.get_counts()
    elif isinstance(result, dict):
        counts = result
    else:
        counts = dict(result)

    heads_count = 0
    tails_count = 0
    total = 0

    for key, value in counts.items():
        count = int(value)
        total += count
        if isinstance(key, int):
            bit = str(key & 1)
        else:
            s = str(key).strip()
            if " " in s:
                s = s.split()[-1]
            bit = s[-1] if s else "0"
        if bit == "0":
            heads_count += count
        elif bit == "1":
            tails_count += count

    for finalize_name in ("finalize", "finalize_qvm"):
        if hasattr(qvm, finalize_name):
            try:
                getattr(qvm, finalize_name)()
                break
            except TypeError:
                pass

    return {"Heads": heads_count / total, "Tails": tails_count / total}
