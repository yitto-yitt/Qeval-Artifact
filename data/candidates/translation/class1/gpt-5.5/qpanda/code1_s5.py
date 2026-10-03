# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import *

def run_bell_state_simulator():
    shots = 1000
    nbits = 2

    def _make_machine():
        if "CPUQVM" in globals():
            m = globals()["CPUQVM"]()
            for name in ("init_qvm", "initQVM", "init"):
                f = getattr(m, name, None)
                if callable(f):
                    try:
                        f()
                        break
                    except TypeError:
                        pass
            return m
        if "init_quantum_machine" in globals() and "QMachineType" in globals():
            qmt = globals()["QMachineType"]
            for typ in ("CPU", "CPU_SINGLE_THREAD", "CPUSingleThread"):
                if hasattr(qmt, typ):
                    return globals()["init_quantum_machine"](getattr(qmt, typ))
        raise RuntimeError("No supported pyQPanda3 quantum machine found")

    def _alloc(machine, kind, count):
        names = (
            ("qAlloc_many", "qalloc_many", "q_alloc_many", "qAllocMany", "qalloc", "allocate_qubits")
            if kind == "q"
            else ("cAlloc_many", "calloc_many", "c_alloc_many", "cAllocMany", "calloc", "allocate_cbits")
        )
        for name in names:
            f = getattr(machine, name, None)
            if callable(f):
                obj = f(count)
                if isinstance(obj, (list, tuple)):
                    return list(obj)
                try:
                    if len(obj) == count:
                        return obj
                except Exception:
                    pass
                return [obj] if count == 1 else obj
        for name in names:
            f = globals().get(name)
            if callable(f):
                obj = f(count)
                return list(obj) if isinstance(obj, (list, tuple)) else obj
        raise RuntimeError("Allocation failed")

    def _append(prog, node):
        if isinstance(node, (list, tuple)):
            for item in node:
                prog = _append(prog, item)
            return prog
        try:
            ret = prog << node
            return prog if ret is None else ret
        except Exception:
            pass
        for name in ("insert", "append", "push_back", "add_gate"):
            f = getattr(prog, name, None)
            if callable(f):
                ret = f(node)
                return prog if ret is None else ret
        raise

    def _prog_class():
        for name in ("QProg", "QProgram", "QCircuit"):
            cls = globals().get(name)
            if cls is not None:
                return cls
        raise RuntimeError("No supported program class found")

    def _cx_gate():
        for name in ("CNOT", "CX"):
            f = globals().get(name)
            if callable(f):
                return f
        raise RuntimeError("No CNOT/CX gate found")

    def _build_unitary(qubits):
        prog = _prog_class()()
        prog = _append(prog, globals()["H"](qubits[0]))
        prog = _append(prog, _cx_gate()(qubits[0], qubits[1]))
        return prog

    def _build_measured(qubits, cbits):
        prog = _build_unitary(qubits)
        m_all = globals().get("measure_all") or globals().get("MeasureAll")
        if callable(m_all):
            prog = _append(prog, m_all(qubits, cbits))
        else:
            meas = globals().get("Measure") or globals().get("MEASURE")
            if not callable(meas):
                raise RuntimeError("No measurement operation found")
            for i in range(nbits):
                prog = _append(prog, meas(qubits[i], cbits[i]))
        return prog

    def _format_key(key):
        if isinstance(key, int):
            return format(key, "0{}b".format(nbits))
        if isinstance(key, str):
            s = key.replace(" ", "")
            if set(s) <= {"0", "1"}:
                return s.zfill(nbits) if len(s) < nbits else s
            bits = "".join(ch for ch in s if ch in "01")
            return bits[-nbits:].zfill(nbits) if bits else s
        if isinstance(key, (list, tuple)):
            return "".join(str(int(x)) for x in key)
        s = str(key)
        bits = "".join(ch for ch in s if ch in "01")
        return bits[-nbits:].zfill(nbits) if bits else s

    def _extract_mapping(result):
        if result is None:
            return None
        if isinstance(result, dict):
            return result
        for name in ("get_counts", "getCounts", "counts", "get_count", "getCount"):
            obj = getattr(result, name, None)
            if callable(obj):
                try:
                    return obj()
                except TypeError:
                    pass
            elif obj is not None:
                return obj
        if isinstance(result, (list, tuple)):
            if all(isinstance(x, (int, float, complex)) for x in result):
                return {format(i, "0{}b".format(nbits)): float(abs(result[i])) for i in range(len(result))}
            try:
                return dict(result)
            except Exception:
                pass
        return None

    def _normalize(mapping):
        data = {}
        for k, v in mapping.items():
            try:
                val = float(v)
            except Exception:
                continue
            if abs(val) > 1e-15:
                data[_format_key(k)] = data.get(_format_key(k), 0.0) + val
        total = sum(data.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in data.items()}

    machine = _make_machine()
    qubits = _alloc(machine, "q", nbits)

    cbits = None
    try:
        cbits = _alloc(machine, "c", nbits)
    except Exception:
        cbits = None

    unitary_prog = _build_unitary(qubits)

    if cbits is not None:
        measured_prog = _build_measured(qubits, cbits)
        run_args = (
            (measured_prog, cbits, shots),
            (measured_prog, shots),
            (measured_prog, cbits),
        )
        for method_name in ("run_with_configuration", "runWithConfiguration", "run_with_config", "run"):
            method = getattr(machine, method_name, None)
            if callable(method):
                for args in run_args:
                    try:
                        mapping = _extract_mapping(method(*args))
                        if mapping:
                            return _normalize(mapping)
                    except Exception:
                        pass

    for method_name in ("prob_run_dict", "probRunDict", "prob_run_list", "probRunList"):
        method = getattr(machine, method_name, None)
        if callable(method):
            for args in ((unitary_prog, qubits, -1), (unitary_prog, qubits), (unitary_prog,)):
                try:
                    mapping = _extract_mapping(method(*args))
                    if mapping:
                        return _normalize(mapping)
                except Exception:
                    pass

    for method_name in ("directly_run", "directlyRun", "execute", "run"):
        method = getattr(machine, method_name, None)
        if callable(method):
            try:
                method(unitary_prog)
                break
            except Exception:
                pass

    for state_name in ("get_qstate", "getQState", "get_state", "getState"):
        get_state = getattr(machine, state_name, None)
        if callable(get_state):
            state = get_state()
            probs = {format(i, "0{}b".format(nbits)): abs(state[i]) ** 2 for i in range(min(len(state), 2 ** nbits))}
            return _normalize(probs)

    raise RuntimeError("Unable to execute pyQPanda3 Bell-state program")
