# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq


def visualize_bell_states():
    shots = 1000

    def _call_first(obj, names, *args):
        last_exc = None
        for name in names:
            if hasattr(obj, name):
                try:
                    return getattr(obj, name)(*args)
                except TypeError as exc:
                    last_exc = exc
        if last_exc is not None:
            raise last_exc
        raise AttributeError(names[0])

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            if hasattr(machine, name):
                return getattr(machine, name)(n)
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            if hasattr(machine, name):
                return [getattr(machine, name)() for _ in range(n)]
        raise AttributeError("qubit allocation method not found")

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
            if hasattr(machine, name):
                return getattr(machine, name)(n)
        for name in ("cAlloc", "calloc", "allocate_cbit"):
            if hasattr(machine, name):
                return [getattr(machine, name)() for _ in range(n)]
        raise AttributeError("cbit allocation method not found")

    def _append_measurements(prog, qubits, cbits):
        if hasattr(pq, "Measure"):
            prog << pq.Measure(qubits[0], cbits[0])
            prog << pq.Measure(qubits[1], cbits[1])
        else:
            prog << pq.measure_all(qubits, cbits)

    def _normalize_counts(raw_counts):
        if not isinstance(raw_counts, dict):
            if hasattr(raw_counts, "get_counts"):
                raw_counts = raw_counts.get_counts()
            else:
                raw_counts = dict(raw_counts)

        counts = {}
        for key, value in raw_counts.items():
            if isinstance(key, int):
                bitstring = format(key, "02b")
            else:
                bitstring = str(key).replace(" ", "")
            counts[bitstring] = counts.get(bitstring, 0) + float(value)

        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    def _run_circuit(phi_minus=False):
        machine = pq.CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "init"):
            machine.init()

        qubits = _alloc_qubits(machine, 2)
        cbits = _alloc_cbits(machine, 2)

        prog = pq.QProg()
        cnot = getattr(pq, "CNOT", None) or getattr(pq, "CX")

        if phi_minus:
            prog << pq.X(qubits[0])
        prog << pq.H(qubits[0])
        prog << cnot(qubits[0], qubits[1])
        _append_measurements(prog, qubits, cbits)

        if hasattr(machine, "run_with_configuration"):
            counts = machine.run_with_configuration(prog, cbits, shots)
        elif hasattr(machine, "run_with_config"):
            counts = machine.run_with_config(prog, cbits, shots)
        else:
            counts = _call_first(machine, ("run",), prog, shots)

        return _normalize_counts(counts)

    return {
        "phi_plus": _run_circuit(False),
        "phi_minus": _run_circuit(True),
    }
