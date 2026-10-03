# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def and_gate(a, b):
    shots = 1024
    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        def _bit_position_map():
            pos_map = {}
            for j in range(3):
                qs = qvm.qAlloc_many(3)
                cs = qvm.cAlloc_many(3)
                prog = QProg()
                prog << X(qs[j])
                for k in range(3):
                    prog << Measure(qs[k], cs[k])
                counts = qvm.run_with_configuration(prog, cs, 1)
                key = next(iter(counts.keys()))
                pos_map[j] = key.index("1")
            return pos_map

        cbit_pos = _bit_position_map()

        qr_a = qvm.qAlloc_many(3)
        qr_b = qvm.qAlloc_many(3)
        ancillary = qvm.qAlloc_many(3)
        measure = qvm.cAlloc_many(3)

        prog = QProg()
        a_bits = format(a, "03b")
        b_bits = format(b, "03b")

        for i in range(3):
            if a_bits[2 - i] == "1":
                prog << X(qr_a[i])
            if b_bits[2 - i] == "1":
                prog << X(qr_b[i])

        for i in range(3):
            prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

        for i in range(3):
            prog << Measure(ancillary[i], measure[i])

        counts = qvm.run_with_configuration(prog, measure, shots)
        total = builtins.sum(counts.values())

        probabilities = {}
        for raw_key, value in counts.items():
            key = raw_key[cbit_pos[2]] + raw_key[cbit_pos[1]] + raw_key[cbit_pos[0]]
            probabilities[key] = probabilities.get(key, 0.0) + value / total

        return probabilities
    finally:
        qvm.finalize()
