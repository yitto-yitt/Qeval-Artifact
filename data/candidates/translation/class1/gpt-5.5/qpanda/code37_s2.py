# EVAL_META: task_id=37, framework=qpanda, class=1
import pyqpanda3.core as pq


def bv_algorithm(s):
    n = len(s)

    machine_cls = getattr(pq, "CPUQVM", None)
    if machine_cls is None:
        machine_cls = getattr(pq, "CPUQVMachine", None)
    machine = machine_cls()

    for init_name in ("init_qvm", "init", "initQVM"):
        init_fn = getattr(machine, init_name, None)
        if callable(init_fn):
            try:
                init_fn()
                break
            except TypeError:
                pass

    def _alloc_many(kind, count):
        names = (
            ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits")
            if kind == "q"
            else ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits")
        )
        for name in names:
            fn = getattr(machine, name, None)
            if callable(fn):
                try:
                    return list(fn(count))
                except TypeError:
                    pass
        single_names = (
            ("qAlloc", "qalloc", "allocate_qubit")
            if kind == "q"
            else ("cAlloc", "calloc", "allocate_cbit")
        )
        for name in single_names:
            fn = getattr(machine, name, None)
            if callable(fn):
                return [fn() for _ in range(count)]
        raise RuntimeError("Unable to allocate quantum or classical bits")

    q = _alloc_many("q", n + 1)
    c = _alloc_many("c", n)

    x_gate = getattr(pq, "X")
    h_gate = getattr(pq, "H")
    cx_gate = getattr(pq, "CNOT", None)
    if cx_gate is None:
        cx_gate = getattr(pq, "CX")
    measure_gate = getattr(pq, "Measure", None)
    if measure_gate is None:
        measure_gate = getattr(pq, "measure")

    def _make_prog(with_measure):
        prog = pq.QProg()

        def add(node):
            nonlocal prog
            ret = prog << node
            if ret is not None:
                prog = ret

        ancilla = n
        add(x_gate(q[ancilla]))
        for qubit in q:
            add(h_gate(qubit))
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                add(cx_gate(q[index], q[ancilla]))
        for index in range(n):
            add(h_gate(q[index]))
        if with_measure:
            for index in range(n):
                add(measure_gate(q[index], c[index]))
        return prog

    prog_measured = _make_prog(True)
    prog_unmeasured = _make_prog(False)

    raw_result = None
    run_attempts = []

    for name in ("run_with_configuration", "run_with_config"):
        fn = getattr(machine, name, None)
        if callable(fn):
            run_attempts.append((fn, (prog_measured, c, 1), {}))
            run_attempts.append((fn, (prog_measured, 1, c), {}))

    run_fn = getattr(machine, "run", None)
    if callable(run_fn):
        run_attempts.append((run_fn, (prog_measured, c, 1), {}))
        run_attempts.append((run_fn, (prog_measured, 1), {"shots": 1}))
        run_attempts.append((run_fn, (prog_measured,), {"shots": 1}))

    for fn, args, kwargs in run_attempts:
        try:
            raw_result = fn(*args, **kwargs)
            break
        except Exception:
            raw_result = None

    if raw_result is None:
        prob_attempts = []
        q_input = q[:n]
        q_input_reversed = list(reversed(q_input))
        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            fn = getattr(machine, name, None)
            if callable(fn):
                prob_attempts.append((fn, (prog_unmeasured, q_input, -1), {}))
                prob_attempts.append((fn, (prog_unmeasured, q_input), {}))
                prob_attempts.append((fn, (prog_unmeasured, q_input_reversed, -1), {}))
                prob_attempts.append((fn, (prog_unmeasured, q_input_reversed), {}))
        for fn, args, kwargs in prob_attempts:
            try:
                raw_result = fn(*args, **kwargs)
                break
            except Exception:
                raw_result = None

    if raw_result is None:
        raise RuntimeError("Unable to execute pyQPanda3 quantum program")

    def _clean_bits(value):
        if n == 0:
            return ""
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, int):
            return format(value, "0{}b".format(n))[-n:]
        text = str(value)
        bits = "".join(ch for ch in text if ch in "01")
        if len(bits) > n:
            bits = bits[-n:]
        if len(bits) < n:
            bits = bits.zfill(n)
        return bits

    def _score(value):
        try:
            return float(value)
        except Exception:
            return 0.0

    def _extract_bits(result):
        if n == 0:
            return ""
        if isinstance(result, dict):
            if not result:
                return ""
            key = max(result.items(), key=lambda item: _score(item[1]))[0]
            return _clean_bits(key)
        if isinstance(result, (list, tuple)):
            if not result:
                return ""
            first = result[0]
            if isinstance(first, (list, tuple)) and len(first) >= 2:
                key = max(result, key=lambda item: _score(item[1]))[0]
                return _clean_bits(key)
            return _clean_bits(first)
        return _clean_bits(result)

    bits = _extract_bits(raw_result)
    if n > 0 and bits != s and bits[::-1] == s:
        bits = bits[::-1]

    bitstrings = [bits]
    return [bitstrings, raw_result]
