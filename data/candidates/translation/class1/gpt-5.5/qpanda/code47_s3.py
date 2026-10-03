# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    shots = int(samples)

    def _init_machine():
        m = pq.CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(m, name, None)
            if callable(method):
                try:
                    method()
                except TypeError:
                    pass
                break
        return m

    def _alloc_many(machine, kind, n):
        if kind == "q":
            many_names = ("qAlloc_many", "qalloc_many", "allocate_qubits", "alloc_qubits", "qAllocMany")
            one_names = ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit")
        else:
            many_names = ("cAlloc_many", "calloc_many", "allocate_cbits", "alloc_cbits", "cAllocMany")
            one_names = ("cAlloc", "calloc", "allocate_cbit", "alloc_cbit")

        for name in many_names:
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    return method(n)
                except TypeError:
                    pass

        allocated = []
        for _ in range(n):
            item = None
            for name in one_names:
                method = getattr(machine, name, None)
                if callable(method):
                    item = method()
                    break
            if item is None:
                raise RuntimeError("Unable to allocate quantum resources")
            allocated.append(item)
        return allocated

    def _build_program(q, c=None, measured=True):
        prog = pq.QProg()
        prog << pq.H(q[0])
        if measured:
            if c is not None:
                try:
                    prog << pq.Measure(q[0], c[0])
                except Exception:
                    prog << pq.measure_all(q, c)
            else:
                prog << pq.measure_all(q)
        return prog

    def _execute_with_counts(machine, prog, c):
        for run_name in ("run_with_configuration", "run_with_config"):
            runner = getattr(machine, run_name, None)
            if callable(runner):
                try:
                    return runner(prog, c, shots)
                except TypeError:
                    try:
                        return runner(prog, c, shots=shots)
                    except TypeError:
                        pass

        runner = getattr(machine, "run", None)
        if callable(runner):
            for args in ((prog, c, shots), (prog, shots)):
                try:
                    result = runner(*args)
                    if result is not None:
                        return result
                except TypeError:
                    pass

        raise RuntimeError("No compatible sampling execution method found")

    def _quick_measure_counts():
        machine = _init_machine()
        q = _alloc_many(machine, "q", 1)
        prog = _build_program(q, None, measured=False)
        directly_run = getattr(machine, "directly_run", None)
        if callable(directly_run):
            directly_run(prog)
        else:
            run = getattr(machine, "run", None)
            if callable(run):
                run(prog)
            else:
                raise RuntimeError("No compatible state execution method found")
        quick_measure = getattr(machine, "quick_measure", None)
        if not callable(quick_measure):
            raise RuntimeError("No compatible measurement method found")
        return quick_measure(q, shots)

    def _normalise_raw_counts(raw):
        if hasattr(raw, "get_counts") and callable(raw.get_counts):
            raw = raw.get_counts()
        elif hasattr(raw, "to_dict") and callable(raw.to_dict):
            raw = raw.to_dict()
        elif isinstance(raw, (list, tuple)) and raw:
            if hasattr(raw[0], "items"):
                raw = raw[0]

        heads = 0.0
        tails = 0.0

        for key, value in raw.items():
            if isinstance(key, bool):
                bit = "1" if key else "0"
            elif isinstance(key, int):
                bit = "1" if key == 1 else "0" if key == 0 else None
            elif isinstance(key, (list, tuple)) and len(key) == 1:
                bit = "1" if int(key[0]) == 1 else "0"
            else:
                s = str(key).strip().replace(" ", "")
                if s in ("0", "False", "false"):
                    bit = "0"
                elif s in ("1", "True", "true"):
                    bit = "1"
                elif len(s) >= 1 and s[-1] in ("0", "1"):
                    bit = s[-1]
                else:
                    bit = None

            if bit == "0":
                heads += float(value)
            elif bit == "1":
                tails += float(value)

        total = heads + tails
        return {"Heads": heads / total, "Tails": tails / total}

    machine = _init_machine()
    q = _alloc_many(machine, "q", 1)
    c = _alloc_many(machine, "c", 1)
    prog = _build_program(q, c, measured=True)

    try:
        counts = _execute_with_counts(machine, prog, c)
    except Exception:
        counts = _quick_measure_counts()

    return _normalise_raw_counts(counts)
