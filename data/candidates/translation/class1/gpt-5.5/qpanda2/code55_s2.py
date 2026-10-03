# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import QMachineType, init_quantum_machine, destroy_quantum_machine, QProg, X, Measure, Toffoli


def or_gate(a, b):
    machine = init_quantum_machine(QMachineType.CPU)
    try:
        bit_positions = {}
        for j in range(3):
            q_cal = machine.qAlloc_many(3)
            c_cal = machine.cAlloc_many(3)
            prog_cal = QProg()
            prog_cal.insert(X(q_cal[j]))
            for k in range(3):
                prog_cal.insert(Measure(q_cal[k], c_cal[k]))
            cal_counts = machine.run_with_configuration(prog_cal, c_cal, 16)
            cal_key = str(max(cal_counts.items(), key=lambda item: item[1])[0])
            ones = [idx for idx, ch in enumerate(cal_key) if ch == "1"]
            if len(ones) == 1:
                bit_positions[j] = ones[0]

        qr_a = machine.qAlloc_many(3)
        qr_b = machine.qAlloc_many(3)
        ancillary = machine.qAlloc_many(3)
        measure = machine.cAlloc_many(3)

        prog = QProg()
        a_bits = format(a, "03b")
        b_bits = format(b, "03b")

        for i in range(3):
            if a_bits[2 - i] == "0":
                prog.insert(X(qr_a[i]))
            if b_bits[2 - i] == "0":
                prog.insert(X(qr_b[i]))

        for i in range(3):
            prog.insert(Toffoli(qr_a[i], qr_b[i], ancillary[i]))

        for i in range(3):
            prog.insert(X(ancillary[i]))

        for i in range(3):
            prog.insert(Measure(ancillary[i], measure[i]))

        shots = 1024
        counts = machine.run_with_configuration(prog, measure, shots)
        total = builtins.sum(counts.values())

        distribution = {}
        for raw_key, value in counts.items():
            raw_key = str(raw_key)
            if all(i in bit_positions for i in range(3)) and len(raw_key) >= 3:
                key = raw_key[bit_positions[2]] + raw_key[bit_positions[1]] + raw_key[bit_positions[0]]
            else:
                key = raw_key
            distribution[key] = distribution.get(key, 0.0) + value / total

        return distribution
    finally:
        destroy_quantum_machine(machine)
