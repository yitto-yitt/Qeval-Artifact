# EVAL_META: task_id=15, framework=qpanda, class=1
import pyqpanda3.core as pq

def noisy_bell():
    def _get_method(obj, names):
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)
        return None

    def _call_init(machine):
        for name in ("init_qvm", "init", "initQVM"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    method()
                    return
                except TypeError:
                    continue

    def _alloc_many(machine, many_names, one_names, count):
        method = _get_method(machine, many_names)
        if method is not None:
            try:
                return list(method(count))
            except TypeError:
                pass
        one = _get_method(machine, one_names)
        if one is None:
            raise RuntimeError("Allocation method not found")
        return [one() for _ in range(count)]

    def _append(prog, op):
        try:
            return prog << op
        except Exception:
            for name in ("insert", "push_back", "append"):
                method = getattr(prog, name, None)
                if method is not None:
                    try:
                        method(op)
                        return prog
                    except Exception:
                        pass
            raise

    def _build_program(qubits, cbits=None):
        prog = pq.QProg()
        prog = _append(prog, pq.H(qubits[0]))
        cnot = getattr(pq, "CNOT", None) or getattr(pq, "CX", None)
        prog = _append(prog, cnot(qubits[0], qubits[1]))
        if cbits is not None:
            meas = getattr(pq, "Measure", None) or getattr(pq, "measure", None)
            prog = _append(prog, meas(qubits[0], cbits[0]))
            prog = _append(prog, meas(qubits[1], cbits[1]))
        return prog

    def _normalize(result, nbits=2):
        if result is None:
            return None
        if hasattr(result, "get_counts"):
            result = result.get_counts()
        if isinstance(result, (list, tuple)) and len(result) == 1 and isinstance(result[0], dict):
            result = result[0]
        if not isinstance(result, dict):
            return None

        dist = {}
        for key, value in result.items():
            if isinstance(key, int):
                bit_key = format(key, "0{}b".format(nbits))
            else:
                bit_key = str(key).strip()
                bits = "".join(ch for ch in bit_key if ch in "01")
                if len(bits) >= nbits:
                    bit_key = bits[-nbits:]
            try:
                val = float(value)
            except Exception:
                continue
            if val > 0:
                dist[bit_key] = dist.get(bit_key, 0.0) + val

        total = sum(dist.values())
        if total <= 0:
            return None
        return {key: value / total for key, value in dist.items() if value / total > 0}

    machine_cls = getattr(pq, "NoiseQVM", None) or getattr(pq, "CPUQVM")
    qvm = machine_cls()
    _call_init(qvm)

    try:
        if hasattr(qvm, "set_noise_model") and hasattr(pq, "NoiseModel") and hasattr(pq, "GateType"):
            noise_model = getattr(pq.NoiseModel, "DEPOLARIZING_KRAUS_OPERATOR", None)
            if noise_model is not None:
                for gate_name, prob in (("HADAMARD_GATE", 0.001), ("H_GATE", 0.001), ("CNOT_GATE", 0.01), ("CX_GATE", 0.01)):
                    gate_type = getattr(pq.GateType, gate_name, None)
                    if gate_type is not None:
                        try:
                            qvm.set_noise_model(noise_model, gate_type, prob)
                        except Exception:
                            pass
    except Exception:
        pass

    qubits = _alloc_many(qvm, ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"), ("qAlloc", "qalloc", "qAlloc_one", "qalloc_one"), 2)
    cbits = _alloc_many(qvm, ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"), ("cAlloc", "calloc", "cAlloc_one", "calloc_one"), 2)

    shots = 1000
    prog_meas = _build_program(qubits, cbits)
    prog = _build_program(qubits, None)

    for name in ("run_with_configuration", "run_with_config", "runWithConfiguration", "sampling", "run"):
        method = getattr(qvm, name, None)
        if method is None:
            continue
        for args in ((prog_meas, cbits, shots), (prog_meas, shots, cbits), (prog_meas, shots)):
            try:
                dist = _normalize(method(*args))
                if dist is not None:
                    return dist
            except Exception:
                pass

    direct = _get_method(qvm, ("directly_run", "directlyRun", "run"))
    quick = _get_method(qvm, ("quick_measure", "quickMeasure"))
    if direct is not None and quick is not None:
        try:
            direct(prog)
            dist = _normalize(quick(qubits, shots))
            if dist is not None:
                return dist
        except Exception:
            pass

    for name in ("prob_run_dict", "probRunDict", "prob_run", "probRun"):
        method = getattr(qvm, name, None)
        if method is None:
            continue
        for args in ((prog, qubits, -1), (prog, qubits)):
            try:
                dist = _normalize(method(*args))
                if dist is not None:
                    return dist
            except Exception:
                pass

    raise RuntimeError("Unable to execute Bell circuit with pyQPanda3")
