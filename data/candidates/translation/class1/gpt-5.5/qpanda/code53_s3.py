# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq

def xor_gate(a, b):
    def _init_machine():
        machine = pq.CPUQVM()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                    break
                except TypeError:
                    pass
        return machine

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        for name in ("qAlloc", "qalloc"):
            if hasattr(machine, name):
                method = getattr(machine, name)
                try:
                    res = method(n)
                    if hasattr(res, "__iter__") and not isinstance(res, (str, bytes)):
                        return list(res)
                except TypeError:
                    pass
                return [method() for _ in range(n)]
        raise RuntimeError("No qubit allocation method found")

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        for name in ("cAlloc", "calloc"):
            if hasattr(machine, name):
                method = getattr(machine, name)
                try:
                    res = method(n)
                    if hasattr(res, "__iter__") and not isinstance(res, (str, bytes)):
                        return list(res)
                except TypeError:
                    pass
                return [method() for _ in range(n)]
        raise RuntimeError("No classical bit allocation method found")

    def _add_measurements(prog, qubits, cbits):
        if hasattr(pq, "Measure"):
            for i in range(len(qubits)):
                prog << pq.Measure(qubits[i], cbits[i])
        else:
            prog << pq.measure_all(qubits, cbits)

    def _run_counts(machine, prog, cbits, shots):
        run = getattr(machine, "run_with_configuration")
        try:
            return run(prog, cbits, shots)
        except TypeError:
            return run(prog, shots, cbits)

    def _normalize_counts(raw_counts):
        if hasattr(raw_counts, "get_counts"):
            raw_counts = raw_counts.get_counts()
        out = {}
        for key, value in dict(raw_counts).items():
            if isinstance(key, bytes):
                key = key.decode()
            elif isinstance(key, int):
                key = format(key, "08b")
            else:
                key = str(key).replace(" ", "")
            if len(key) > 8:
                key = key[-8:]
            out[key] = out.get(key, 0) + value
        return out

    shots = 1024
    machine = _init_machine()

    cal_q = _alloc_qubits(machine, 8)
    cal_c = _alloc_cbits(machine, 8)
    cal_prog = pq.QProg()
    cal_prog << pq.X(cal_q[0])
    _add_measurements(cal_prog, cal_q, cal_c)
    cal_counts = _normalize_counts(_run_counts(machine, cal_prog, cal_c, shots))
    cal_key = max(cal_counts, key=cal_counts.get)
    reverse_keys = len(cal_key) >= 8 and cal_key[0] == "1"

    qubits = _alloc_qubits(machine, 8)
    cbits = _alloc_cbits(machine, 8)
    prog = pq.QProg()

    for value in (int(a), int(b)):
        for i in range(8):
            if (value >> i) & 1:
                prog << pq.X(qubits[i])

    _add_measurements(prog, qubits, cbits)
    counts = _normalize_counts(_run_counts(machine, prog, cbits, shots))

    total = sum(counts.values())
    if reverse_keys:
        return {key[::-1]: value / total for key, value in counts.items()}
    return {key: value / total for key, value in counts.items()}
