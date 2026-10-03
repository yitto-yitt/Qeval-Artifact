# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq

def sampler_qiskit() -> Dict[str, float]:
    def _get_method(obj, names):
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)
        return None

    def _format_key(key, nbits=2):
        if isinstance(key, str):
            s = key.replace(" ", "")
            if set(s) <= {"0", "1"}:
                return s.zfill(nbits)
            try:
                return format(int(s), "0{}b".format(nbits))
            except Exception:
                return s
        if isinstance(key, int):
            return format(key, "0{}b".format(nbits))
        if isinstance(key, (list, tuple)):
            return "".join(str(int(x)) for x in key).zfill(nbits)
        return str(key).zfill(nbits)

    def _normalize(result):
        if isinstance(result, dict):
            items = result.items()
        else:
            items = result

        probs = {}
        for k, v in items:
            try:
                val = float(v)
            except Exception:
                continue
            if val > 1e-12:
                probs[_format_key(k, 2)] = probs.get(_format_key(k, 2), 0.0) + val

        total = sum(probs.values())
        if total > 0:
            probs = {k: v / total for k, v in probs.items()}
        return probs

    qvm = pq.CPUQVM()
    try:
        init = _get_method(qvm, ("init_qvm", "initQVM", "init"))
        if init is not None:
            try:
                init()
            except TypeError:
                pass

        for seed_name in ("set_random_seed", "setRandomSeed", "set_rng_seed", "setRngSeed"):
            seed_func = _get_method(qvm, (seed_name,))
            if seed_func is not None:
                try:
                    seed_func(42)
                except Exception:
                    pass

        qalloc = _get_method(qvm, ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"))
        qubits = qalloc(2)

        H = getattr(pq, "H")
        CNOT = getattr(pq, "CNOT", getattr(pq, "CX", None))

        prog = pq.QProg()
        prog << H(qubits[0])
        prog << CNOT(qubits[0], qubits[1])

        for method_name in ("prob_run_dict", "probRunDict"):
            method = _get_method(qvm, (method_name,))
            if method is not None:
                for args in ((prog, qubits, -1), (prog, qubits)):
                    try:
                        probs = _normalize(method(*args))
                        if probs:
                            return probs
                    except Exception:
                        pass

        direct = _get_method(qvm, ("directly_run", "directlyRun"))
        if direct is not None:
            try:
                direct(prog)
                for method_name in ("get_prob_dict", "getProbDict", "pmeasure_bin_index", "pMeasureBinIndex"):
                    method = _get_method(qvm, (method_name,))
                    if method is not None:
                        for args in ((qubits, -1), (qubits,)):
                            try:
                                probs = _normalize(method(*args))
                                if probs:
                                    return probs
                            except Exception:
                                pass
            except Exception:
                pass

        calloc = _get_method(qvm, ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"))
        cbits = calloc(2)

        prog_meas = pq.QProg()
        prog_meas << H(qubits[0])
        prog_meas << CNOT(qubits[0], qubits[1])

        measure_all = getattr(pq, "measure_all", None)
        if measure_all is not None:
            try:
                prog_meas << measure_all(qubits, cbits)
            except Exception:
                measure_all = None

        if measure_all is None:
            Measure = getattr(pq, "Measure")
            prog_meas << Measure(qubits[0], cbits[0])
            prog_meas << Measure(qubits[1], cbits[1])

        run = _get_method(qvm, ("run_with_configuration", "runWithConfiguration"))
        counts = run(prog_meas, cbits, 4096)
        return _normalize(counts)

    finally:
        finalize = _get_method(qvm, ("finalize", "finalize_qvm", "finalizeQVM"))
        if finalize is not None:
            try:
                finalize()
            except Exception:
                pass
