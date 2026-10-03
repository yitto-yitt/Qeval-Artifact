# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import *

def not_gate(a):
    def _init_machine():
        m = CPUQVM()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(m, name):
                getattr(m, name)()
                break
        return m

    def _alloc_q(m, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        raise RuntimeError("No qubit allocation method available")

    def _alloc_c(m, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        raise RuntimeError("No classical bit allocation method available")

    def _size(v):
        try:
            return len(v)
        except Exception:
            return v.size()

    def _clean_key(k, n):
        if isinstance(k, int):
            return format(k, "0{}b".format(n))
        if isinstance(k, (list, tuple)):
            return "".join(str(int(x)) for x in k)
        s = str(k).strip().replace(" ", "")
        if s.startswith("0b"):
            s = s[2:]
        if len(s) < n:
            s = s.zfill(n)
        return s[-n:]

    def _normalize_dict(d, n):
        out = {}
        for k, v in d.items():
            val = float(v)
            if val > 1e-12:
                out[_clean_key(k, n)] = out.get(_clean_key(k, n), 0.0) + val
        total = sum(out.values())
        return {k: v / total for k, v in out.items()} if total else out

    def _probabilities(m, prog, qbits):
        n = _size(qbits)
        for args in ((prog, qbits, -1), (prog, qbits)):
            if hasattr(m, "prob_run_dict"):
                try:
                    return _normalize_dict(m.prob_run_dict(*args), n)
                except Exception:
                    pass
            fn = globals().get("prob_run_dict")
            if fn is not None:
                try:
                    return _normalize_dict(fn(*args), n)
                except Exception:
                    pass

        cbits = _alloc_c(m, n)
        ma = globals().get("measure_all")
        measured = False
        if ma is not None:
            try:
                prog << ma(qbits, cbits)
                measured = True
            except Exception:
                measured = False
        if not measured:
            for i in range(n):
                prog << Measure(qbits[i], cbits[i])

        shots = 1024
        counts = None
        for name in ("run_with_configuration", "runWithConfiguration"):
            if hasattr(m, name):
                runner = getattr(m, name)
                for args in ((prog, cbits, shots), (prog, shots, cbits)):
                    try:
                        counts = runner(*args)
                        break
                    except Exception:
                        pass
            if counts is not None:
                break
        if counts is None:
            fn = globals().get("run_with_configuration")
            if fn is not None:
                for args in ((prog, cbits, shots), (prog, shots, cbits)):
                    try:
                        counts = fn(*args)
                        break
                    except Exception:
                        pass
        if counts is None:
            raise RuntimeError("No executable probability or sampling method available")
        return _normalize_dict(counts, n)

    mcal = _init_machine()
    qcal = _alloc_q(mcal, 2)
    pcal = QProg()
    pcal << X(qcal[0])
    cal = _probabilities(mcal, pcal, qcal)
    cal_key = max(cal, key=cal.get)
    left_is_first = cal_key[0] == "1"

    m = _init_machine()
    q = _alloc_q(m, 8)
    prog = QProg()
    bits = format(a, "08b")
    for i in range(8):
        if bits[7 - i] == "0":
            prog << X(q[i])

    raw = _probabilities(m, prog, q)
    result = {}
    for k, v in raw.items():
        key = k[::-1] if left_is_first else k
        result[key] = result.get(key, 0.0) + v
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
