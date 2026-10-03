# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq

def xor_gate(a, b):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qv = qvm.qAlloc_many(8)
    cv = qvm.cAlloc_many(8)
    circuit = pq.QCircuit()
    for i in range(8):
        if (a >> i) & 1:
            circuit << pq.X(qv[i])
        if (b >> i) & 1:
            circuit << pq.X(qv[i])
    prog = pq.QProg()
    prog << circuit
    for i in range(8):
        prog << pq.Measure(qv[i], cv[i])
    result = qvm.run_with_configuration(prog, shots=1024)
    total = sum(result.values())
    return {key: val / total for key, val in result.items()}
