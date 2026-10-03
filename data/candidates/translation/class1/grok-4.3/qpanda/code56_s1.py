# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq

def not_gate(a):
    qvm = pq.CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = pq.QProg()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7 - i] == "0":
            prog << pq.X(qubits[i])
    prog << pq.measure_all(qubits, cbits)
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
