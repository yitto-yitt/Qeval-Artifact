# EVAL_META: task_id=130, framework=qpanda, class=3
import pyqpanda3.core as pq

def inv_circuit(n):
    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(n)
    else:
        q = qvm.qalloc_many(n)

    if not hasattr(inv_circuit, "_qvms"):
        inv_circuit._qvms = []
    inv_circuit._qvms.append(qvm)

    qc = pq.QCircuit()

    def append_gate(circuit, gate):
        try:
            circuit << gate
        except Exception:
            circuit.insert(gate)

    for i in range(1, -1, -1):
        append_gate(qc, pq.CNOT(q[i + 1], q[i + 3]))

    for i in range(1, -1, -1):
        append_gate(qc, pq.H(q[i + 1]))

    return qc
