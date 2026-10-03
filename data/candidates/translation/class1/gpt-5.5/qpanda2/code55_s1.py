# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        def _dominant_key(counts):
            return max(counts, key=counts.get)

        raw_positions = {}
        for bit_index in range(3):
            qcal = machine.qAlloc_many(3)
            ccal = machine.cAlloc_many(3)
            cal_prog = pq.QProg()
            cal_prog << pq.X(qcal[bit_index])
            for j in range(3):
                cal_prog << pq.Measure(qcal[j], ccal[j])
            cal_counts = machine.run_with_configuration(cal_prog, ccal, 1)
            cal_key = _dominant_key(cal_counts)
            raw_positions[bit_index] = cal_key.find("1")

        qr_a = machine.qAlloc_many(3)
        qr_b = machine.qAlloc_many(3)
        ancillary = machine.qAlloc_many(3)
        measure = machine.cAlloc_many(3)

        prog = pq.QProg()
        a_bits = format(a, "03b")
        b_bits = format(b, "03b")

        for i in range(3):
            if a_bits[2 - i] == "0":
                prog << pq.X(qr_a[i])
            if b_bits[2 - i] == "0":
                prog << pq.X(qr_b[i])

        for i in range(3):
            prog << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])

        for i in range(3):
            prog << pq.X(ancillary[i])

        for i in range(3):
            prog << pq.Measure(ancillary[i], measure[i])

        shots = 1024
        counts = machine.run_with_configuration(prog, measure, shots)
        total = builtins.sum(counts.values())

        probabilities = {}
        for raw_key, value in counts.items():
            key = (
                raw_key[raw_positions[2]]
                + raw_key[raw_positions[1]]
                + raw_key[raw_positions[0]]
            )
            probabilities[key] = probabilities.get(key, 0.0) + value / total

        return probabilities
    finally:
        machine.finalize()
