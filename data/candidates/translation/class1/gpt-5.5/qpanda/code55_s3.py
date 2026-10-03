# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq

def or_gate(a, b):
    def _make_machine():
        if hasattr(pq, "CPUQVM"):
            qvm = pq.CPUQVM()
        elif hasattr(pq, "CPUSingleThreadQVM"):
            qvm = pq.CPUSingleThreadQVM()
        elif hasattr(pq, "init_quantum_machine"):
            qtype = getattr(getattr(pq, "QMachineType", object), "CPU", None)
            qvm = pq.init_quantum_machine(qtype) if qtype is not None else pq.init_quantum_machine()
        else:
            qvm = pq.QuantumMachine()
        for name in ("init_qvm", "initQVM", "init"):
            if hasattr(qvm, name):
                try:
                    getattr(qvm, name)()
                    break
                except TypeError:
                    pass
        return qvm

    def _alloc_qubits(qvm, n):
        for name in ("qAlloc_many", "qAllocMany", "qalloc_many", "qallocMany", "allocateQubits"):
            if hasattr(qvm, name):
                return list(getattr(qvm, name)(n))
        for name in ("qAlloc", "qalloc", "allocateQubit"):
            if hasattr(qvm, name):
                return [getattr(qvm, name)() for _ in range(n)]
        raise RuntimeError("No qubit allocation method found")

    def _alloc_cbits(qvm, n):
        for name in ("cAlloc_many", "cAllocMany", "calloc_many", "callocMany", "allocateCBits"):
            if hasattr(qvm, name):
                return list(getattr(qvm, name)(n))
        for name in ("cAlloc", "calloc", "allocateCBit"):
            if hasattr(qvm, name):
                return [getattr(qvm, name)() for _ in range(n)]
        raise RuntimeError("No classical bit allocation method found")

    def _add(prog, op):
        if op is None:
            return
        try:
            prog << op
        except Exception:
            if hasattr(prog, "insert"):
                prog.insert(op)
            elif hasattr(prog, "append"):
                prog.append(op)
            else:
                raise

    def _x_gate(q):
        return pq.X(q)

    def _ccx_gate(c1, c2, t):
        for name in ("Toffoli", "CCX", "CCNOT", "TOFFOLI"):
            if hasattr(pq, name):
                return getattr(pq, name)(c1, c2, t)
        gate = pq.X(t)
        if hasattr(gate, "control"):
            controlled = gate.control([c1, c2])
            return gate if controlled is None else controlled
        if hasattr(gate, "set_control"):
            controlled = gate.set_control([c1, c2])
            return gate if controlled is None else controlled
        raise RuntimeError("No controlled-controlled-X gate method found")

    def _measure_gate(q, c):
        for name in ("Measure", "measure"):
            if hasattr(pq, name):
                return getattr(pq, name)(q, c)
        raise RuntimeError("No measurement method found")

    def _clean_counts(res, n):
        if hasattr(res, "get_counts"):
            res = res.get_counts()
        if not isinstance(res, dict):
            if hasattr(res, "items"):
                res = dict(res.items())
            else:
                raise RuntimeError("Unsupported result type")
        out = {}
        for k, v in res.items():
            if isinstance(k, int):
                key = format(k, "0{}b".format(n))
            else:
                key = str(k).replace(" ", "")
                if key.startswith("0b"):
                    key = key[2:]
                if len(key) < n:
                    key = key.zfill(n)
                elif len(key) > n:
                    key = key[-n:]
            val = float(v)
            if val != 0.0:
                out[key] = out.get(key, 0.0) + val
        return out

    def _run_counts(qvm, prog, cbits, shots, n):
        for name in ("run_with_configuration", "runWithConfiguration", "run_with_config"):
            if hasattr(qvm, name):
                meth = getattr(qvm, name)
                for args in ((prog, cbits, shots), (prog, shots, cbits)):
                    try:
                        return _clean_counts(meth(*args), n)
                    except Exception:
                        pass
        for name in ("run",):
            if hasattr(qvm, name):
                meth = getattr(qvm, name)
                for args in ((prog, cbits, shots), (prog, shots, cbits), (prog, shots)):
                    try:
                        return _clean_counts(meth(*args), n)
                    except Exception:
                        pass
        raise RuntimeError("No executable shot-based run method found")

    def _detect_list_order(qvm):
        try:
            q = _alloc_qubits(qvm, 2)
            c = _alloc_cbits(qvm, 2)
            prog = pq.QProg()
            _add(prog, _x_gate(q[0]))
            _add(prog, _measure_gate(q[0], c[0]))
            _add(prog, _measure_gate(q[1], c[1]))
            counts = _run_counts(qvm, prog, c, 64, 2)
            key = max(counts, key=counts.get)
            if key == "10":
                return True
            if key == "01":
                return False
        except Exception:
            pass
        return True

    qvm = _make_machine()
    list_order = _detect_list_order(qvm)

    qubits = _alloc_qubits(qvm, 9)
    cbits = _alloc_cbits(qvm, 3)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    prog = pq.QProg()

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "0":
            _add(prog, _x_gate(qr_a[i]))
        if b_bits[2 - i] == "0":
            _add(prog, _x_gate(qr_b[i]))

    for i in range(3):
        _add(prog, _ccx_gate(qr_a[i], qr_b[i], ancillary[i]))

    for i in range(3):
        _add(prog, _x_gate(ancillary[i]))

    if list_order:
        _add(prog, _measure_gate(ancillary[2], cbits[0]))
        _add(prog, _measure_gate(ancillary[1], cbits[1]))
        _add(prog, _measure_gate(ancillary[0], cbits[2]))
    else:
        _add(prog, _measure_gate(ancillary[0], cbits[0]))
        _add(prog, _measure_gate(ancillary[1], cbits[1]))
        _add(prog, _measure_gate(ancillary[2], cbits[2]))

    counts = _run_counts(qvm, prog, cbits, 1024, 3)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
