# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq

def and_gate(a, b):
    def _make_machine():
        cls = getattr(pq, "CPUQVM", None)
        if cls is None:
            cls = getattr(pq, "QVM", None)
        machine = cls()
        for name in ("init_qvm", "init", "initQVM"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    method()
                except TypeError:
                    pass
                break
        return machine

    def _vec_to_list(vec, n):
        try:
            return [vec[i] for i in range(n)]
        except Exception:
            return list(vec)

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "alloc_qubits"):
            method = getattr(machine, name, None)
            if method is not None:
                return _vec_to_list(method(n), n)
        for name in ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"):
            method = getattr(machine, name, None)
            if method is not None:
                return [method() for _ in range(n)]
        raise RuntimeError("Cannot allocate qubits")

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "allocate_cbits", "alloc_cbits"):
            method = getattr(machine, name, None)
            if method is not None:
                return _vec_to_list(method(n), n)
        for name in ("cAlloc", "calloc", "allocate_cbit", "alloc_cbit"):
            method = getattr(machine, name, None)
            if method is not None:
                return [method() for _ in range(n)]
        raise RuntimeError("Cannot allocate cbits")

    def _append(prog, node):
        insert = getattr(prog, "insert", None)
        if insert is not None:
            ret = insert(node)
            return ret if ret is not None else prog
        prog << node
        return prog

    def _x_gate(q):
        for name in ("X", "x"):
            fn = getattr(pq, name, None)
            if callable(fn):
                return fn(q)
        raise RuntimeError("X gate not found")

    def _ccx_gate(c0, c1, target):
        for name in ("Toffoli", "TOFFOLI", "CCX", "ccx", "toffoli"):
            fn = getattr(pq, name, None)
            if callable(fn):
                return fn(c0, c1, target)
        gate = _x_gate(target)
        ctrl = getattr(gate, "control", None)
        if ctrl is not None:
            return ctrl([c0, c1])
        raise RuntimeError("CCX/Toffoli gate not found")

    def _measure_gate(q, c):
        for name in ("Measure", "measure"):
            fn = getattr(pq, name, None)
            if callable(fn):
                return fn(q, c)
        raise RuntimeError("Measure gate not found")

    def _counts_from_result(res):
        if isinstance(res, dict):
            return dict(res)
        get_counts = getattr(res, "get_counts", None)
        if get_counts is not None:
            return dict(get_counts())
        result = getattr(res, "result", None)
        if callable(result):
            return _counts_from_result(result())
        raise TypeError("Unsupported result type")

    def _run_counts(machine, prog, cbits, shots):
        for name in ("run_with_configuration", "runWithConfiguration", "run_with_config"):
            method = getattr(machine, name, None)
            if method is not None:
                for args in ((prog, cbits, shots), (prog, shots, cbits), (prog, shots)):
                    try:
                        return _counts_from_result(method(*args))
                    except TypeError:
                        continue
        for name in ("run",):
            method = getattr(machine, name, None)
            if method is not None:
                for args in ((prog, cbits, shots), (prog, shots, cbits), (prog, shots)):
                    try:
                        return _counts_from_result(method(*args))
                    except TypeError:
                        continue
        direct = getattr(machine, "directly_run", None)
        if direct is not None:
            counts = {}
            for _ in range(shots):
                direct(prog)
                bits = []
                for cb in cbits:
                    val = None
                    for n in ("get_val", "getValue", "get_value"):
                        m = getattr(cb, n, None)
                        if m is not None:
                            val = m()
                            break
                    if val is None:
                        get_cbit_value = getattr(machine, "get_cbit_value", None)
                        if get_cbit_value is not None:
                            val = get_cbit_value(cb)
                    bits.append("1" if int(val) else "0")
                key = "".join(bits)
                counts[key] = counts.get(key, 0) + 1
            return counts
        raise RuntimeError("No executable run method found")

    def _clean_key(key):
        s = str(key).replace(" ", "")
        if len(s) >= 3:
            return s[-3:]
        return s.zfill(3)

    def _calibrate_positions(machine):
        positions = [None, None, None]
        for idx in range(3):
            q = _alloc_qubits(machine, 3)
            c = _alloc_cbits(machine, 3)
            prog = pq.QProg()
            prog = _append(prog, _x_gate(q[idx]))
            for j in range(3):
                prog = _append(prog, _measure_gate(q[j], c[j]))
            counts = _run_counts(machine, prog, c, 8)
            key = _clean_key(max(counts, key=counts.get))
            if key.count("1") != 1:
                return [2, 1, 0]
            positions[idx] = key.index("1")
        if sorted(positions) != [0, 1, 2]:
            return [2, 1, 0]
        return positions

    machine = _make_machine()
    pos_for_cbit = _calibrate_positions(machine)

    qubits = _alloc_qubits(machine, 9)
    cbits = _alloc_cbits(machine, 3)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]

    prog = pq.QProg()
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "1":
            prog = _append(prog, _x_gate(qr_a[i]))
        if b_bits[2 - i] == "1":
            prog = _append(prog, _x_gate(qr_b[i]))

    for i in range(3):
        prog = _append(prog, _ccx_gate(qr_a[i], qr_b[i], ancillary[i]))

    for i in range(3):
        prog = _append(prog, _measure_gate(ancillary[i], cbits[i]))

    shots = 1024
    counts = _run_counts(machine, prog, cbits, shots)
    total = float(sum(counts.values()))
    distribution = {}

    for raw_key, value in counts.items():
        key = _clean_key(raw_key)
        qiskit_key = key[pos_for_cbit[2]] + key[pos_for_cbit[1]] + key[pos_for_cbit[0]]
        distribution[qiskit_key] = distribution.get(qiskit_key, 0.0) + float(value) / total

    return distribution
