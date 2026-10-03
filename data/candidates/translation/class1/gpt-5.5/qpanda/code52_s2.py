# EVAL_META: task_id=52, framework=qpanda, class=1
import pyqpanda3.core as pq


def send_bits(bitstring):
    def _cnot():
        gate = getattr(pq, "CNOT", None)
        if gate is None:
            gate = getattr(pq, "CX")
        return gate

    def _measure_nodes(q0, q1, c0, c1):
        measure = getattr(pq, "Measure", None)
        if measure is None:
            measure = getattr(pq, "measure", None)
        if measure is not None:
            return [measure(q0, c0), measure(q1, c1)]
        measure_all = getattr(pq, "measure_all", None)
        if measure_all is None:
            measure_all = getattr(pq, "MeasureAll")
        return [measure_all([q0, q1], [c0, c1])]

    def _build(q0, q1, c0, c1):
        prog = pq.QProg()
        cnot = _cnot()

        prog << pq.H(q0)
        prog << cnot(q0, q1)

        if bitstring[1] == "1":
            prog << pq.Z(q0)
        if bitstring[0] == "1":
            prog << pq.X(q0)

        prog << cnot(q0, q1)
        prog << pq.H(q0)

        for node in _measure_nodes(q0, q1, c0, c1):
            prog << node
        return prog

    try:
        return _build(0, 1, 0, 1)
    except Exception:
        qvm_cls = getattr(pq, "CPUQVM", None)
        if qvm_cls is None:
            qvm_cls = getattr(pq, "CpuQVM")
        qvm = qvm_cls()

        for init_name in ("init_qvm", "initQVM", "init"):
            init = getattr(qvm, init_name, None)
            if init is not None:
                init()
                break

        qalloc = getattr(qvm, "qAlloc_many", None)
        if qalloc is None:
            qalloc = getattr(qvm, "qalloc_many", None)
        calloc = getattr(qvm, "cAlloc_many", None)
        if calloc is None:
            calloc = getattr(qvm, "calloc_many", None)

        q = qalloc(2)
        c = calloc(2)

        if not hasattr(send_bits, "_machines"):
            send_bits._machines = []
        send_bits._machines.append(qvm)

        return _build(q[0], q[1], c[0], c[1])
