# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    counts = qvm.run_with_configuration(prog, c, 1000)
    qvm.finalize()

    total = sum(counts.values())
    result = {}
    for key, value in counts.items():
        if isinstance(key, str):
            if all(ch in "01" for ch in key):
                bitstring = key.zfill(2)
            else:
                bitstring = format(int(key), "02b")
        else:
            bitstring = format(int(key), "02b")
        result[bitstring] = value / total

    return result
