# EVAL_META: task_id=14, framework=qpanda, class=1
import random
import pyqpanda3.core as pq


def bell_each_shot():
    shots = 10

    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "initQVM", "init"):
        if hasattr(machine, init_name):
            try:
                getattr(machine, init_name)()
            except TypeError:
                pass
            break

    q_alloc = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"):
        if hasattr(machine, name):
            q_alloc = getattr(machine, name)
            break
    if q_alloc is None:
        raise RuntimeError("No qubit allocation method found")

    c_alloc = None
    for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany", "allocate_cbits"):
        if hasattr(machine, name):
            c_alloc = getattr(machine, name)
            break
    if c_alloc is None:
        raise RuntimeError("No classical bit allocation method found")

    qubits = q_alloc(2)
    cbits = c_alloc(2)

    cnot_gate = getattr(pq, "CNOT", None)
    if cnot_gate is None:
        cnot_gate = getattr(pq, "CX")

    def make_prog(with_measurements):
        prog = pq.QProg()

        def add(op):
            nonlocal prog
            try:
                prog << op
            except Exception:
                if hasattr(prog, "insert"):
                    prog.insert(op)
                else:
                    prog = prog << op

        add(pq.H(qubits[0]))
        add(cnot_gate(qubits[0], qubits[1]))

        if with_measurements:
            measure_all = getattr(pq, "measure_all", None)
            if measure_all is None:
                measure_all = getattr(pq, "MeasureAll", None)
            if measure_all is not None:
                try:
                    add(measure_all(qubits, cbits))
                except Exception:
                    add(pq.Measure(qubits[0], cbits[0]))
                    add(pq.Measure(qubits[1], cbits[1]))
            else:
                add(pq.Measure(qubits[0], cbits[0]))
                add(pq.Measure(qubits[1], cbits[1]))

        return prog

    def bit_key(key):
        if isinstance(key, str):
            s = key.replace(" ", "")
            bits = "".join(ch for ch in s if ch in "01")
            if bits:
                s = bits
        elif isinstance(key, int):
            s = format(key, "02b")
        elif isinstance(key, (list, tuple)):
            s = "".join(str(int(x)) for x in key)
        else:
            s = str(key).replace(" ", "")
            bits = "".join(ch for ch in s if ch in "01")
            if bits:
                s = bits
        if len(s) < 2:
            s = s.zfill(2)
        elif len(s) > 2:
            s = s[-2:]
        return s

    def normalize_counts(raw):
        if hasattr(raw, "get_counts"):
            raw = raw.get_counts()
        if isinstance(raw, list):
            counts = {}
            for item in raw:
                k = bit_key(item)
                counts[k] = counts.get(k, 0) + 1
        elif isinstance(raw, dict):
            counts = {}
            for k, v in raw.items():
                kk = bit_key(k)
                counts[kk] = counts.get(kk, 0) + float(v)
        else:
            return None

        counts = {k: v for k, v in counts.items() if v > 1e-12}
        total = sum(counts.values())
        if total <= 0:
            return None
        return {k: v / total for k, v in counts.items()}

    measured_prog = make_prog(True)

    for method_name in ("run_with_configuration", "runWithConfiguration", "run_with_config"):
        if hasattr(machine, method_name):
            method = getattr(machine, method_name)
            for args in ((measured_prog, cbits, shots), (measured_prog, shots, cbits)):
                try:
                    dist = normalize_counts(method(*args))
                    if dist is not None:
                        return dist
                except Exception:
                    pass
            try:
                dist = normalize_counts(method(measured_prog, cbits, shots=shots))
                if dist is not None:
                    return dist
            except Exception:
                pass

    for method_name in ("run", "run_prog", "runProg"):
        if hasattr(machine, method_name):
            method = getattr(machine, method_name)
            for args in ((measured_prog, shots), (measured_prog,)):
                try:
                    dist = normalize_counts(method(*args))
                    if dist is not None:
                        return dist
                except Exception:
                    pass
            try:
                dist = normalize_counts(method(measured_prog, shots=shots))
                if dist is not None:
                    return dist
            except Exception:
                pass

    unitary_prog = make_prog(False)

    probabilities = None
    for method_name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list", "probRunTupleList"):
        if hasattr(machine, method_name):
            method = getattr(machine, method_name)
            for args in ((unitary_prog, qubits, -1), (unitary_prog, qubits), (unitary_prog, qubits, 2)):
                try:
                    probabilities = method(*args)
                    break
                except Exception:
                    pass
        if probabilities is not None:
            break

    prob_dist = normalize_counts(probabilities)
    if prob_dist is None:
        raise RuntimeError("Unable to execute quantum program")

    keys = list(prob_dist.keys())
    weights = [prob_dist[k] for k in keys]
    total_w = sum(weights)
    weights = [w / total_w for w in weights]

    counts = {}
    for _ in range(shots):
        r = random.random()
        acc = 0.0
        chosen = keys[-1]
        for k, w in zip(keys, weights):
            acc += w
            if r <= acc:
                chosen = k
                break
        counts[chosen] = counts.get(chosen, 0) + 1

    return {k: v / shots for k, v in counts.items()}
