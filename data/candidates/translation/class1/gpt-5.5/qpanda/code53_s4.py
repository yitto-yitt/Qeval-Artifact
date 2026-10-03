# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import *
import pyqpanda3.core as pq
import numbers

def xor_gate(a, b):
    n = 8

    def _get(name):
        return getattr(pq, name, globals().get(name, None))

    qvm_cls = _get("CPUQVM")
    qvm = qvm_cls()

    for init_name in ("init_qvm", "init", "initQVM"):
        init_func = getattr(qvm, init_name, None)
        if callable(init_func):
            try:
                init_func()
                break
            except TypeError:
                pass
            except Exception:
                pass

    def _alloc_qubits(machine, count):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "allocateQubits", "qAllocMany"):
            func = getattr(machine, name, None)
            if callable(func):
                try:
                    return func(count)
                except TypeError:
                    pass
        func = getattr(machine, "qAlloc", None)
        if callable(func):
            try:
                return [func() for _ in range(count)]
            except TypeError:
                return func(count)
        raise RuntimeError("Unable to allocate qubits")

    def _alloc_cbits(machine, count):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits", "allocateCbits", "cAllocMany"):
            func = getattr(machine, name, None)
            if callable(func):
                try:
                    return func(count)
                except TypeError:
                    pass
        func = getattr(machine, "cAlloc", None)
        if callable(func):
            try:
                return [func() for _ in range(count)]
            except TypeError:
                return func(count)
        raise RuntimeError("Unable to allocate cbits")

    def _new_prog():
        prog_cls = _get("QProg")
        return prog_cls()

    def _append_x(prog, qubit):
        x_gate = _get("X")
        prog << x_gate(qubit)

    def _key_to_string(key, width):
        if isinstance(key, (bytes, bytearray)):
            key = key.decode()
        if isinstance(key, str):
            s = key.strip().replace(" ", "")
            if s.startswith(("0x", "0X")):
                s = format(int(s, 16), "b")
            elif s.startswith(("0b", "0B")):
                s = s[2:]
            else:
                s = "".join(ch for ch in s if ch in "01")
            if len(s) < width:
                s = s.zfill(width)
            elif len(s) > width:
                s = s[-width:]
            return s
        if isinstance(key, numbers.Integral):
            return format(int(key) & ((1 << width) - 1), "0{}b".format(width))
        try:
            s = "".join(str(int(x)) for x in key)
            if len(s) < width:
                s = s.zfill(width)
            elif len(s) > width:
                s = s[-width:]
            return s
        except Exception:
            s = str(key)
            s = "".join(ch for ch in s if ch in "01")
            if len(s) < width:
                s = s.zfill(width)
            elif len(s) > width:
                s = s[-width:]
            return s

    def _normalize(raw, width, reverse_bits=False):
        items = []
        if hasattr(raw, "items"):
            items = list(raw.items())
        elif isinstance(raw, (list, tuple)):
            if all(isinstance(x, numbers.Number) for x in raw):
                items = list(enumerate(raw))
            else:
                for x in raw:
                    if isinstance(x, (list, tuple)) and len(x) >= 2:
                        items.append((x[0], x[1]))
        result = {}
        for key, value in items:
            prob = float(value.real if isinstance(value, complex) else value)
            if abs(prob) <= 1e-15:
                continue
            s = _key_to_string(key, width)
            if reverse_bits:
                s = s[::-1]
            result[s] = result.get(s, 0.0) + prob
        total = sum(result.values())
        if total != 0:
            result = {k: v / total for k, v in result.items()}
        return result

    def _run_prob(machine, prog, qubits):
        for name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list", "probRunTupleList"):
            func = getattr(machine, name, None)
            if callable(func):
                for args in ((prog, qubits, -1), (prog, qubits), (prog, qubits, 0), (prog, qubits, 256)):
                    try:
                        return func(*args)
                    except TypeError:
                        pass
                    except Exception:
                        pass
        for name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list", "probRunTupleList"):
            func = _get(name)
            if callable(func):
                for args in ((prog, qubits, -1), (prog, qubits), (prog, qubits, 0), (prog, qubits, 256)):
                    try:
                        return func(*args)
                    except TypeError:
                        pass
                    except Exception:
                        pass
        return None

    def _needs_reverse(machine, qubits):
        cal_prog = _new_prog()
        _append_x(cal_prog, qubits[0])
        raw = _run_prob(machine, cal_prog, qubits)
        if raw is None:
            return False
        dist = _normalize(raw, n, False)
        if not dist:
            return False
        key = max(dist, key=dist.get)
        return key == ("1" + "0" * (n - 1))

    qubits = _alloc_qubits(qvm, n)
    prog = _new_prog()

    for i in range(n):
        if (int(a) >> i) & 1:
            _append_x(prog, qubits[i])
    for i in range(n):
        if (int(b) >> i) & 1:
            _append_x(prog, qubits[i])

    raw_probs = _run_prob(qvm, prog, qubits)
    if raw_probs is not None:
        reverse = _needs_reverse(qvm, qubits)
        dist = _normalize(raw_probs, n, reverse)
        if dist:
            return dist

    cbits = _alloc_cbits(qvm, n)

    def _append_measurements(program, qs, cs):
        meas_all = _get("measure_all")
        if callable(meas_all):
            try:
                program << meas_all(qs, cs)
                return
            except Exception:
                pass
        meas = _get("Measure") or _get("measure")
        for i in range(n):
            program << meas(qs[i], cs[i])

    _append_measurements(prog, qubits, cbits)
    shots = 1024

    raw_counts = None
    for name in ("run_with_configuration", "runWithConfiguration"):
        func = getattr(qvm, name, None)
        if callable(func):
            for args in ((prog, cbits, shots), (prog, shots, cbits)):
                try:
                    raw_counts = func(*args)
                    break
                except TypeError:
                    pass
                except Exception:
                    pass
            if raw_counts is not None:
                break

    if raw_counts is None:
        for name in ("run_with_configuration", "runWithConfiguration"):
            func = _get(name)
            if callable(func):
                for args in ((prog, cbits, shots), (prog, shots, cbits)):
                    try:
                        raw_counts = func(*args)
                        break
                    except TypeError:
                        pass
                    except Exception:
                        pass
                if raw_counts is not None:
                    break

    if raw_counts is None:
        raise RuntimeError("Unable to execute quantum program")

    return _normalize(raw_counts, n, False)
