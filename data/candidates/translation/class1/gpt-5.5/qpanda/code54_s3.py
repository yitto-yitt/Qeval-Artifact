# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq

def and_gate(a, b):
    def _new_machine():
        cls = getattr(pq, "CPUQVM", None)
        if cls is None:
            raise RuntimeError("CPUQVM is not available in pyqpanda3.core")
        machine = cls()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                    break
                except TypeError:
                    pass
        return machine

    def _qalloc_many(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(machine, name):
                qv = getattr(machine, name)(n)
                try:
                    return list(qv)
                except TypeError:
                    return [qv[i] for i in range(n)]
        raise RuntimeError("No compatible qubit allocation method found")

    def _make_qvec(items):
        if hasattr(pq, "QVec"):
            try:
                return pq.QVec(items)
            except Exception:
                try:
                    v = pq.QVec()
                    for item in items:
                        if hasattr(v, "append"):
                            v.append(item)
                        elif hasattr(v, "push_back"):
                            v.push_back(item)
                    return v
                except Exception:
                    pass
        return items

    def _append(prog, op):
        try:
            res = prog << op
            return prog if res is None else res
        except Exception:
            if hasattr(prog, "insert"):
                res = prog.insert(op)
                return prog if res is None else res
            raise

    def _x(qubit):
        gate = getattr(pq, "X", None)
        if gate is None:
            gate = getattr(pq, "x")
        return gate(qubit)

    def _ccx(c1, c2, target):
        for name in ("Toffoli", "TOFFOLI", "CCX", "ccx"):
            if hasattr(pq, name):
                return getattr(pq, name)(c1, c2, target)
        gate = _x(target)
        if hasattr(gate, "control"):
            controlled = gate.control([c1, c2])
            return gate if controlled is None else controlled
        raise RuntimeError("No compatible CCX/Toffoli gate found")

    def _normalize_key(key, n):
        if isinstance(key, int):
            return format(key, "0{}b".format(n))
        s = "".join(ch for ch in str(key) if ch in "01")
        if len(s) < n:
            s = s.zfill(n)
        elif len(s) > n:
            s = s[-n:]
        return s

    def _as_distribution(raw, n):
        dist = {}
        if isinstance(raw, dict):
            iterable = raw.items()
        else:
            iterable = enumerate(raw)
        for key, val in iterable:
            try:
                p = float(val)
            except Exception:
                continue
            k = _normalize_key(key, n)
            dist[k] = dist.get(k, 0.0) + p
        total = sum(dist.values())
        if total != 0:
            dist = {k: v / total for k, v in dist.items() if v / total > 1e-12}
        return dist

    def _run_prob(machine, prog, qubits, n):
        qargs = []
        qv = _make_qvec(qubits)
        qargs.append(qv)
        if qv is not qubits:
            qargs.append(qubits)

        for method_name in ("prob_run_dict", "prob_run_list", "prob_run_tuple_list"):
            if hasattr(machine, method_name):
                method = getattr(machine, method_name)
                for qarg in qargs:
                    for args in ((prog, qarg, -1), (prog, qarg)):
                        try:
                            return _as_distribution(method(*args), n)
                        except Exception:
                            pass

        for run_name in ("directly_run", "direct_run", "run"):
            if hasattr(machine, run_name):
                getattr(machine, run_name)(prog)
                break

        for method_name in ("pmeasure", "pmeasure_no_index", "PMeasure"):
            if hasattr(machine, method_name):
                method = getattr(machine, method_name)
                for qarg in qargs:
                    try:
                        return _as_distribution(method(qarg), n)
                    except Exception:
                        pass

        raise RuntimeError("No compatible probability execution method found")

    def _calibration_positions():
        positions = []
        for idx in range(3):
            machine = _new_machine()
            q = _qalloc_many(machine, 3)
            prog = pq.QProg()
            prog = _append(prog, _x(q[idx]))
            dist = _run_prob(machine, prog, [q[0], q[1], q[2]], 3)
            key = max(dist, key=dist.get)
            pos = key.find("1")
            if pos < 0:
                return [2, 1, 0]
            positions.append(pos)
        if sorted(positions) != [0, 1, 2]:
            return [2, 1, 0]
        return positions

    positions = _calibration_positions()

    machine = _new_machine()
    qr_a = _qalloc_many(machine, 3)
    qr_b = _qalloc_many(machine, 3)
    ancillary = _qalloc_many(machine, 3)
    prog = pq.QProg()

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "1":
            prog = _append(prog, _x(qr_a[i]))
        if b_bits[2 - i] == "1":
            prog = _append(prog, _x(qr_b[i]))

    for i in range(3):
        prog = _append(prog, _ccx(qr_a[i], qr_b[i], ancillary[i]))

    raw_dist = _run_prob(machine, prog, [ancillary[0], ancillary[1], ancillary[2]], 3)

    result = {}
    for raw_key, prob in raw_dist.items():
        logical = ["0", "0", "0"]
        for i, pos in enumerate(positions):
            logical[i] = raw_key[pos]
        key = logical[2] + logical[1] + logical[0]
        result[key] = result.get(key, 0.0) + prob

    total = sum(result.values())
    return {k: v / total for k, v in result.items() if total and v / total > 1e-12}
