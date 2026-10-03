# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    def _attr(obj, names):
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val):
                    try:
                        val = val()
                    except TypeError:
                        pass
                return val
        return None

    def _is_qubit_sequence(obj):
        if obj is None or isinstance(obj, (str, bytes)):
            return False
        try:
            items = list(obj)
        except Exception:
            return False
        if not items:
            return False
        return hasattr(items[0], "get_phy_addr") or "Qubit" in type(items[0]).__name__

    def _qaddr(q):
        if hasattr(q, "get_phy_addr"):
            return q.get_phy_addr()
        return 0

    def _make_qvec(items):
        try:
            v = QVec()
            for item in items:
                v.append(item)
            return v
        except Exception:
            return items

    def _extract(obj):
        circ = obj
        qv = None
        machine = None
        n = None

        if isinstance(obj, (tuple, list)):
            for item in obj:
                if isinstance(item, int):
                    n = item
                elif _is_qubit_sequence(item):
                    qv = list(item)
                elif hasattr(item, "qAlloc_many") or hasattr(item, "prob_run_dict"):
                    machine = item
                else:
                    circ = item
        else:
            n = _attr(obj, ("num_qubits", "n_qubits", "nqubits", "qubit_num", "num_qbits", "n"))
            qv_attr = _attr(obj, ("qubits", "qbits", "qvec", "qv", "q", "qubit_list"))
            if _is_qubit_sequence(qv_attr):
                qv = list(qv_attr)
            machine = _attr(obj, ("machine", "qvm", "quantum_machine"))
            for name in ("circuit", "qcircuit", "program", "prog", "qc"):
                if hasattr(obj, name):
                    candidate = getattr(obj, name)
                    if callable(candidate):
                        try:
                            candidate = candidate()
                        except TypeError:
                            pass
                    if candidate is not obj:
                        circ = candidate
                        break

        if n is None:
            try:
                n = int(_attr(circ, ("num_qubits", "n_qubits", "nqubits", "qubit_num", "num_qbits", "n")))
            except Exception:
                n = None

        if qv is None:
            qv_attr = _attr(circ, ("qubits", "qbits", "qvec", "qv", "q", "qubit_list"))
            if _is_qubit_sequence(qv_attr):
                qv = list(qv_attr)

        if qv is None:
            getter = globals().get("get_all_used_qubits")
            if getter is not None:
                try:
                    qv = sorted(list(getter(circ)), key=_qaddr)
                except Exception:
                    qv = None

        if n is None and qv is not None:
            n = len(qv)

        return circ, qv, machine, n

    circuit, qubits, machine, n = _extract(oracle)

    if qubits is None and n is not None:
        try:
            qubits = list(qAlloc_many(n))
        except Exception:
            if "init" in globals():
                init(QMachineType.CPU)
            qubits = list(qAlloc_many(n))

    if callable(circuit) and qubits is not None:
        built = circuit(_make_qvec(qubits))
        if built is not None:
            circuit, new_qubits, new_machine, new_n = _extract(built)
            if new_qubits is not None:
                qubits = new_qubits
            if new_machine is not None:
                machine = new_machine
            if new_n is not None:
                n = new_n

    if n is None:
        n = len(qubits)

    qubits = list(qubits)[:n]

    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])
    prog << circuit
    for i in range(n):
        prog << H(qubits[i])

    input_qubits = _make_qvec(qubits[:n - 1])

    if machine is not None and hasattr(machine, "prob_run_dict"):
        raw = machine.prob_run_dict(prog, input_qubits, -1)
    else:
        raw = prob_run_dict(prog, input_qubits, -1)

    probs = {}
    for key, value in raw.items():
        if isinstance(key, int):
            out_key = format(key, "0{}b".format(n - 1))
        else:
            out_key = str(key)
        try:
            prob = float(value)
        except Exception:
            prob = float(abs(value))
        if prob > 1e-12:
            probs[out_key] = prob

    total = builtins.sum(probs.values())
    if total != 0:
        probs = {key: value / total for key, value in probs.items()}
    return probs
