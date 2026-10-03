# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq


def visualize_bell_states():
    shots = 1000

    def _new_qvm():
        if hasattr(pq, "CPUQVM"):
            qvm = pq.CPUQVM()
        elif hasattr(pq, "init_quantum_machine") and hasattr(pq, "QMachineType"):
            qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
        else:
            raise RuntimeError("No supported pyQPanda3 QVM available")

        for name in ("init_qvm", "init", "initialize"):
            if hasattr(qvm, name):
                try:
                    getattr(qvm, name)()
                    break
                except TypeError:
                    pass
        return qvm

    def _alloc_many(qvm, names, count):
        for name in names:
            if hasattr(qvm, name):
                return list(getattr(qvm, name)(count))
        raise RuntimeError("No supported allocator available")

    def _bit_key(key, width=2):
        if isinstance(key, str):
            s = key.replace(" ", "").replace(",", "")
            if len(s) >= width and all(ch in "01" for ch in s[-width:]):
                return s[-width:]
            return s
        if isinstance(key, int):
            return format(key, "0{}b".format(width))[-width:]
        if isinstance(key, (tuple, list)):
            return "".join(str(int(x)) for x in key)
        return str(key)

    def _normalize(raw, width=2):
        if hasattr(raw, "get_counts"):
            raw = raw.get_counts()

        data = {}
        if isinstance(raw, dict):
            iterable = raw.items()
        elif isinstance(raw, (list, tuple)):
            if all(isinstance(x, (int, float, complex)) for x in raw):
                iterable = [(format(i, "0{}b".format(width)), x) for i, x in enumerate(raw)]
            else:
                counts = {}
                for item in raw:
                    if isinstance(item, str):
                        counts[item] = counts.get(item, 0) + 1
                    elif isinstance(item, (tuple, list)) and len(item) == 2:
                        counts[item[0]] = counts.get(item[0], 0) + item[1]
                iterable = counts.items()
        else:
            return None

        for k, v in iterable:
            try:
                val = float(v.real if hasattr(v, "real") else v)
            except Exception:
                continue
            if abs(val) > 1e-12:
                data[_bit_key(k, width)] = data.get(_bit_key(k, width), 0.0) + val

        total = sum(data.values())
        if total <= 0:
            return None
        return {k: v / total for k, v in data.items() if v / total > 1e-12}

    def _append_gates(prog, qubits, minus):
        if minus:
            prog << pq.X(qubits[0])
        prog << pq.H(qubits[0])
        if hasattr(pq, "CNOT"):
            prog << pq.CNOT(qubits[0], qubits[1])
        else:
            prog << pq.CX(qubits[0], qubits[1])
        return prog

    def _make_programs(qvm, minus):
        qubits = _alloc_many(qvm, ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"), 2)
        cbits = _alloc_many(qvm, ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"), 2)

        state_prog = pq.QProg()
        _append_gates(state_prog, qubits, minus)

        meas_prog = pq.QProg()
        _append_gates(meas_prog, qubits, minus)
        if hasattr(pq, "measure_all"):
            meas_prog << pq.measure_all(qubits, cbits)
        elif hasattr(pq, "MeasureAll"):
            meas_prog << pq.MeasureAll(qubits, cbits)
        else:
            for i in range(2):
                meas_prog << pq.Measure(qubits[i], cbits[i])

        return qubits, cbits, state_prog, meas_prog

    def _run_state(minus):
        qvm = _new_qvm()
        qubits, cbits, state_prog, meas_prog = _make_programs(qvm, minus)

        for method_name in ("run_with_configuration", "runWithConfiguration", "run_with_config"):
            if hasattr(qvm, method_name):
                method = getattr(qvm, method_name)
                for args in ((meas_prog, cbits, shots), (meas_prog, shots, cbits)):
                    try:
                        dist = _normalize(method(*args), 2)
                        if dist:
                            return dist
                    except Exception:
                        pass

        if hasattr(qvm, "run"):
            for args in ((meas_prog, cbits, shots), (meas_prog, shots), (meas_prog, cbits)):
                try:
                    dist = _normalize(qvm.run(*args), 2)
                    if dist:
                        return dist
                except Exception:
                    pass

        for method_name in ("prob_run_dict", "probRunDict"):
            if hasattr(qvm, method_name):
                method = getattr(qvm, method_name)
                for args in ((state_prog, qubits, -1), (state_prog, qubits), (state_prog, qubits, 4)):
                    try:
                        dist = _normalize(method(*args), 2)
                        if dist:
                            return dist
                    except Exception:
                        pass

        for method_name in ("prob_run_list", "probRunList"):
            if hasattr(qvm, method_name):
                method = getattr(qvm, method_name)
                for args in ((state_prog, qubits, -1), (state_prog, qubits), (state_prog, qubits, 4)):
                    try:
                        dist = _normalize(method(*args), 2)
                        if dist:
                            return dist
                    except Exception:
                        pass

        if hasattr(qvm, "directly_run"):
            try:
                qvm.directly_run(state_prog)
            except Exception:
                pass
        elif hasattr(qvm, "directlyRun"):
            try:
                qvm.directlyRun(state_prog)
            except Exception:
                pass

        for method_name in ("get_prob_dict", "getProbDict", "pmeasure", "PMeasure"):
            if hasattr(qvm, method_name):
                method = getattr(qvm, method_name)
                for args in ((qubits, -1), (qubits,), (qubits, 4)):
                    try:
                        dist = _normalize(method(*args), 2)
                        if dist:
                            return dist
                    except Exception:
                        pass

        raise RuntimeError("Unable to execute pyQPanda3 quantum program")

    return {
        "phi_plus": _run_state(False),
        "phi_minus": _run_state(True),
    }
