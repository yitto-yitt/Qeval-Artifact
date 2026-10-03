# EVAL_META: task_id=15, framework=qpanda, class=1
import pyqpanda3.core as pq


def noisy_bell():
    def _init_qvm(qvm):
        for name in ("init_qvm", "init", "initialize"):
            if hasattr(qvm, name):
                getattr(qvm, name)()
                return

    def _alloc_qubits(qvm, n):
        for name in ("qAlloc_many", "qalloc_many", "q_alloc_many"):
            if hasattr(qvm, name):
                return getattr(qvm, name)(n)
        return list(range(n))

    def _alloc_cbits(qvm, n):
        for name in ("cAlloc_many", "calloc_many", "c_alloc_many"):
            if hasattr(qvm, name):
                return getattr(qvm, name)(n)
        return None

    def _cnot(control, target):
        gate = getattr(pq, "CNOT", None) or getattr(pq, "CX", None)
        return gate(control, target)

    def _make_prog(qubits, cbits=None):
        prog = pq.QProg()
        prog << pq.H(qubits[0])
        prog << _cnot(qubits[0], qubits[1])
        if cbits is not None:
            if hasattr(pq, "Measure"):
                prog << pq.Measure(qubits[0], cbits[0])
                prog << pq.Measure(qubits[1], cbits[1])
            elif hasattr(pq, "measure"):
                prog << pq.measure(qubits[0], cbits[0])
                prog << pq.measure(qubits[1], cbits[1])
            elif hasattr(pq, "measure_all"):
                prog << pq.measure_all(qubits, cbits)
        return prog

    def _normalize(result):
        if hasattr(result, "items"):
            data = dict(result.items())
        else:
            data = dict(result)
        total = float(sum(data.values()))
        if total == 0.0:
            return {}
        return {str(k): float(v) / total for k, v in data.items()}

    qvm = pq.CPUQVM()
    _init_qvm(qvm)
    qubits = _alloc_qubits(qvm, 2)
    cbits = _alloc_cbits(qvm, 2)

    if cbits is not None:
        measured_prog = _make_prog(qubits, cbits)
        if hasattr(qvm, "run_with_configuration"):
            try:
                result = qvm.run_with_configuration(measured_prog, cbits, 1000)
                return _normalize(result)
            except TypeError:
                try:
                    result = qvm.run_with_configuration(measured_prog, 1000, cbits)
                    return _normalize(result)
                except TypeError:
                    pass

    prog = _make_prog(qubits, None)
    if hasattr(qvm, "prob_run_dict"):
        try:
            return _normalize(qvm.prob_run_dict(prog, qubits, -1))
        except TypeError:
            return _normalize(qvm.prob_run_dict(prog, qubits))

    if hasattr(qvm, "run"):
        try:
            return _normalize(qvm.run(prog, 1000))
        except TypeError:
            return _normalize(qvm.run(prog))

    raise RuntimeError("No compatible pyQPanda3 execution method found")
