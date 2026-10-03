# EVAL_META: task_id=92, framework=qpanda, class=1
import pyqpanda3.core as pq

def calculate_stabilizer_state_info():
    def _clean_probabilities(raw, nbits=2):
        out = {}

        if isinstance(raw, dict):
            iterable = raw.items()
        else:
            try:
                raw_list = list(raw)
            except TypeError:
                raw_list = []
            if raw_list and all(not isinstance(x, (tuple, list)) for x in raw_list):
                iterable = enumerate(raw_list)
            else:
                iterable = raw_list

        for item in iterable:
            if isinstance(item, (tuple, list)) and len(item) == 2:
                a, b = item
                if isinstance(a, str):
                    key, val = a, b
                elif isinstance(b, str):
                    key, val = b, a
                else:
                    key, val = a, b
            else:
                continue

            try:
                p = float(val)
            except TypeError:
                p = float(val.real)

            if abs(p) <= 1e-12:
                continue

            if isinstance(key, str):
                bitstr = key.replace(" ", "")
                if set(bitstr) <= {"0", "1"}:
                    bitstr = bitstr.zfill(nbits)
            else:
                bitstr = format(int(key), "0{}b".format(nbits))

            pr = round(p, 12)
            out[bitstr] = pr if abs(p - pr) <= 1e-12 else p

        return dict(sorted(out.items()))

    qvm = pq.CPUQVM()

    for init_name in ("init_qvm", "init"):
        init_fn = getattr(qvm, init_name, None)
        if callable(init_fn):
            try:
                init_fn()
                break
            except Exception:
                pass

    q = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        alloc_fn = getattr(qvm, alloc_name, None)
        if callable(alloc_fn):
            try:
                q = alloc_fn(2)
                break
            except Exception:
                pass

    if q is None:
        qubits = []
        for alloc_name in ("qAlloc", "qalloc", "allocate_qubit"):
            alloc_fn = getattr(qvm, alloc_name, None)
            if callable(alloc_fn):
                qubits = [alloc_fn(), alloc_fn()]
                break
        q = qubits

    prog = pq.QProg()

    h_gate = getattr(pq, "H")(q[0])
    cnot_ctor = getattr(pq, "CNOT", None)
    if cnot_ctor is None:
        cnot_ctor = getattr(pq, "CX")
    cx_gate = cnot_ctor(q[0], q[1])

    for gate in (h_gate, cx_gate):
        try:
            prog << gate
        except Exception:
            prog.insert(gate)

    for provider in (qvm, pq):
        prob_fn = getattr(provider, "prob_run_dict", None)
        if callable(prob_fn):
            for args in ((prog, q, -1), (prog, q)):
                try:
                    return _clean_probabilities(prob_fn(*args), 2)
                except Exception:
                    pass

    executed = False
    for run_name in ("directly_run", "run", "execute"):
        run_fn = getattr(qvm, run_name, None)
        if callable(run_fn):
            try:
                run_fn(prog)
                executed = True
                break
            except Exception:
                pass

    if executed:
        for prob_name in ("get_prob_dict", "get_probabilities", "pmeasure"):
            prob_fn = getattr(qvm, prob_name, None)
            if callable(prob_fn):
                for args in ((q, -1), (q,), ()):
                    try:
                        return _clean_probabilities(prob_fn(*args), 2)
                    except Exception:
                        pass

        for state_name in ("get_qstate", "get_qstate_vector", "get_state"):
            state_fn = getattr(qvm, state_name, None)
            if callable(state_fn):
                try:
                    state = state_fn()
                    if isinstance(state, dict):
                        return _clean_probabilities({k: abs(complex(v)) ** 2 for k, v in state.items()}, 2)
                    probs = {}
                    for i, amp in enumerate(list(state)):
                        probs[format(i, "02b")] = abs(complex(amp)) ** 2
                    return _clean_probabilities(probs, 2)
                except Exception:
                    pass

    raise RuntimeError("Unable to compute probabilities with pyQPanda3")
