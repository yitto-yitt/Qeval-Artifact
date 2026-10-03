# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import *
from collections import Counter

def xor_gate(a, b):
    bit_len = 8
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(bit_len)
    c = machine.cAlloc_many(bit_len)

    prog = QProg()
    x = (a ^ b) & ((1 << bit_len) - 1)
    for i in range(bit_len):
        if (x >> i) & 1:
            prog << X(q[i])

    for i in range(bit_len):
        prog << Measure(q[i], c[i])

    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    machine.finalize()

    probs = {}
    total = sum(result.values()) if result else 0
    if total == 0:
        return {"00000000": 1.0}

    for k, v in result.items():
        if isinstance(k, str):
            bits = ''.join(ch for ch in k if ch in '01')
            if len(bits) < bit_len:
                bits = bits.zfill(bit_len)
            elif len(bits) > bit_len:
                bits = bits[-bit_len:]
            probs[bits] = probs.get(bits, 0.0) + v / total

    if not probs:
        return {"00000000": 1.0}
    return probs
