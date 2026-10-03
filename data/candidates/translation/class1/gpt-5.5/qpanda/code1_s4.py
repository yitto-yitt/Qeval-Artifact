# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import *


def run_bell_state_simulator():
    def _call_first(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)(*args)
        raise AttributeError(names[0])

    def _bitstring_from_key(key, width=2):
        if isinstance(key, str):
            s = "".join(ch for ch in key if ch in "01")
            if len(s) == width:
                return s
            try:
                return format(int(key), "0{}b".format(width))[-width:]
            except Exception:
                return s.zfill(width)[-width:]
        try:
            return format(int(key), "0{}b".format(width))[-width:]
        except Exception:
            return str(key)

    def _normalize_distribution(raw, width=2):
        if hasattr(raw, "items"):
            items = list(raw.items())
        elif isinstance(raw, (list, tuple)) and all(not isinstance(x, (list, tuple, dict)) for x in raw):
            items = list(enumerate(raw))
        else:
            items = list(raw)

        dist = {}
        for item in items:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                key, value = item[0], item[1]
            else:
                continue
            try:
                value = float(value)
            except Exception:
                continue
            if value > 1e-12:
                bitstring = _bitstring_from_key(key, width)
                dist[bitstring] = dist.get(bitstring, 0.0) + value

        total = sum(dist.values())
        if total == 0:
            return {}
        return {key: value / total for key, value in dist.items()}

    def _build_program(qubits):
        prog = QProg()
        prog << H(qubits[0])
        cnot = globals().get("CNOT", globals().get("CX"))
        prog << cnot(qubits[0], qubits[1])
        return prog

    def _add_measurements(prog, qubits, cbits):
        meas_all = globals().get("measure_all", globals().get("MeasureAll"))
        if meas_all is not None:
            prog << meas_all(qubits, cbits)
        else:
            meas = globals().get("Measure")
            for i in range(2):
                prog << meas(qubits[i], cbits[i])
        return prog

    qvm = CPUQVM()
    try:
        if hasattr(qvm, "init_qvm"):
            qvm.init_qvm()
        elif hasattr(qvm, "init"):
            qvm.init()

        qubits = _call_first(qvm, ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"), 2)
        try:
            cbits = _call_first(qvm, ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"), 2)
        except Exception:
            cbits = None

        prog = _build_program(qubits)

        for method_name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            if hasattr(qvm, method_name):
                method = getattr(qvm, method_name)
                for args in ((prog, qubits, -1), (prog, qubits)):
                    try:
                        return _normalize_distribution(method(*args), 2)
                    except Exception:
                        pass

        for run_name in ("directly_run", "run"):
            if hasattr(qvm, run_name):
                try:
                    getattr(qvm, run_name)(prog)
                    break
                except Exception:
                    pass

        for method_name in ("get_prob_dict", "get_prob_tuple_list", "get_prob_list", "pmeasure"):
            if hasattr(qvm, method_name):
                method = getattr(qvm, method_name)
                for args in ((qubits, -1), (qubits,)):
                    try:
                        dist = _normalize_distribution(method(*args), 2)
                        if dist:
                            return dist
                    except Exception:
                        pass

        pmeasure = globals().get("PMeasure")
        if pmeasure is not None:
            for args in ((qubits, -1), (qubits,)):
                try:
                    dist = _normalize_distribution(pmeasure(*args), 2)
                    if dist:
                        return dist
                except Exception:
                    pass

        if cbits is None:
            cbits = _call_first(qvm, ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"), 2)

        measured_prog = _add_measurements(_build_program(qubits), qubits, cbits)

        raw_counts = None
        if hasattr(qvm, "run_with_configuration"):
            for args in ((measured_prog, cbits, 1000), (measured_prog, 1000)):
                try:
                    raw_counts = qvm.run_with_configuration(*args)
                    break
                except Exception:
                    pass

        if raw_counts is None and globals().get("run_with_configuration") is not None:
            for args in ((measured_prog, cbits, 1000), (measured_prog, 1000)):
                try:
                    raw_counts = globals()["run_with_configuration"](*args)
                    break
                except Exception:
                    pass

        return _normalize_distribution(raw_counts, 2)
    finally:
        if hasattr(qvm, "finalize"):
            try:
                qvm.finalize()
            except Exception:
                pass
        elif hasattr(qvm, "finalize_qvm"):
            try:
                qvm.finalize_qvm()
            except Exception:
                pass
