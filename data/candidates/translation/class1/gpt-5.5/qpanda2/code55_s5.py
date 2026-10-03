# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def or_gate(a, b):
    shots = 1024
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        def _cbit_position(cbit_index):
            q_cal = machine.qAlloc_many(3)
            c_cal = machine.cAlloc_many(3)
            prog_cal = pq.QProg()
            prog_cal << pq.X(q_cal[cbit_index])
            for j in range(3):
                prog_cal << pq.Measure(q_cal[j], c_cal[j])
            counts_cal = machine.run_with_configuration(prog_cal, c_cal, 1)
            key = next(iter(counts_cal.keys())).replace(" ", "")
            return key.index("1")

        positions = [_cbit_position(i) for i in range(3)]

        qr_a = machine.qAlloc_many(3)
        qr_b = machine.qAlloc_many(3)
        ancillary = machine.qAlloc_many(3)
        measure = machine.cAlloc_many(3)

        prog = pq.QProg()
        a = format(a, "03b")
        b = format(b, "03b")

        for i in range(3):
            if a[2 - i] == "0":
                prog << pq.X(qr_a[i])
            if b[2 - i] == "0":
                prog << pq.X(qr_b[i])

        for i in range(3):
            prog << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])

        for i in range(3):
            prog << pq.X(ancillary[i])

        for i in range(3):
            prog << pq.Measure(ancillary[i], measure[i])

        counts = machine.run_with_configuration(prog, measure, shots)
        total = builtins.sum(counts.values())

        probabilities = {}
        for key, value in counts.items():
            key = key.replace(" ", "")
            out_key = key[positions[2]] + key[positions[1]] + key[positions[0]]
            probabilities[out_key] = probabilities.get(out_key, 0.0) + value / total

        return probabilities
    finally:
        machine.finalize()
