# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq


def sampler_qiskit():
    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "init", "initQVM"):
        if hasattr(machine, init_name):
            try:
                getattr(machine, init_name)()
                break
            except TypeError:
                pass

    for seed_name in ("set_random_seed", "set_random_seed_simulator", "set_seed", "seed"):
        if hasattr(machine, seed_name):
            try:
                getattr(machine, seed_name)(42)
                break
            except Exception:
                pass

    q = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        if hasattr(machine, alloc_name):
            q = getattr(machine, alloc_name)(2)
            break
    if q is None:
        q = [machine.qAlloc(), machine.qAlloc()]

    prog = pq.QProg()

    def append(inst):
        nonlocal prog
        try:
            prog = prog << inst
        except Exception:
            prog.insert(inst)

    append(pq.H(q[0]))
    if hasattr(pq, "CNOT"):
        append(pq.CNOT(q[0], q[1]))
    else:
        append(pq.CX(q[0], q[1]))

    def normalize_distribution(raw):
        if not isinstance(raw, dict):
            raw = dict(raw)
        out = {}
        for key, value in raw.items():
            if isinstance(key, int):
                bitstring = format(key, "02b")
            else:
                bitstring = str(key).replace(" ", "")
                if bitstring.startswith("0x"):
                    bitstring = format(int(bitstring, 16), "02b")
                elif bitstring.startswith("0b"):
                    bitstring = bitstring[2:].zfill(2)
                else:
                    bitstring = bitstring.zfill(2)
            prob = float(value.real if hasattr(value, "real") else value)
            if prob > 1e-12:
                out[bitstring[-2:]] = prob
        total = sum(out.values())
        return {k: v / total for k, v in out.items()} if total else out

    for method_name in ("prob_run_dict", "prob_run_dict_with_no_index"):
        if hasattr(machine, method_name):
            method = getattr(machine, method_name)
            for args in ((prog, q, -1), (prog, q), (prog, q, 2)):
                try:
                    return normalize_distribution(method(*args))
                except Exception:
                    pass

    for run_name in ("directly_run", "run"):
        if hasattr(machine, run_name):
            try:
                getattr(machine, run_name)(prog)
                for prob_name in ("get_prob_dict", "get_probabilities", "pmeasure_bin_index"):
                    if hasattr(machine, prob_name):
                        prob_method = getattr(machine, prob_name)
                        for args in ((q, -1), (q,), (q, 2)):
                            try:
                                return normalize_distribution(prob_method(*args))
                            except Exception:
                                pass
            except Exception:
                pass

    c = None
    for calloc_name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
        if hasattr(machine, calloc_name):
            c = getattr(machine, calloc_name)(2)
            break
    if c is None:
        c = [machine.cAlloc(), machine.cAlloc()]

    if hasattr(pq, "measure_all"):
        append(pq.measure_all(q, c))
    else:
        append(pq.Measure(q[0], c[0]))
        append(pq.Measure(q[1], c[1]))

    for run_conf_name in ("run_with_configuration", "runWithConfiguration"):
        if hasattr(machine, run_conf_name):
            counts = getattr(machine, run_conf_name)(prog, c, 4096)
            total = sum(counts.values())
            return {str(k).zfill(2)[-2:]: v / total for k, v in counts.items() if v}

    raise RuntimeError("No compatible pyQPanda3 execution method found")
