# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QCircuit, QProg, X, Measure

def not_gate(a):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(8)
    c = qvm.cAlloc_many(8)

    circuit = QCircuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7 - i] == "0":
            circuit << X(q[i])

    for i in range(8):
        circuit << Measure(q[i], c[i])

    prog = QProg()
    prog << circuit

    counts = qvm.run_with_configuration(prog, c, 1024)
    total = sum(counts.values())

    dist = {}
    for key, value in counts.items():
        if isinstance(key, int):
            bitstr = format(key, "08b")
        else:
            bitstr = str(key).zfill(8)
        dist[bitstr] = value / total

    return dist
