# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq
def not_gate(a):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = pq.QProg()
    a = format(a, "08b")
    for i in range(8):
        if a[7-i] == "0":
            prog.insert(pq.X(qubits[i]))
    for i in range(8):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    total = sum(result.values())
    return {format(key, "08b"): value / total for key, value in result.items()}
