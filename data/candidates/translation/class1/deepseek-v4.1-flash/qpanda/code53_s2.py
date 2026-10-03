# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, Measure


def xor_gate(a, b):
    def run_counts(prog, shots):
        qvm = CPUQVM()
        if hasattr(qvm, "init_qvm"):
            qvm.init_qvm()
        res = qvm.run(prog, shots)
        if not isinstance(res, dict) and not hasattr(res, "get_counts"):
            res = qvm.result()
        return res if isinstance(res, dict) else res.get_counts()

    # Calibrate which position of a measurement string holds which qubit.
    pos_to_qubit = [0] * 8
    for k in range(8):
        cal = QProg()
        cal << X(k)
        for i in range(8):
            cal << Measure(i, i)
        counts = run_counts(cal, 1)
        key = max(counts, key=lambda s: counts[s])
        pos_to_qubit[key.index("1")] = k

    # XOR(8, a) then XOR(8, b): X on qubit i whenever bit i of a^b is set.
    value = a ^ b
    prog = QProg()
    for i in range(8):
        if (value >> i) & 1:
            prog << X(i)
    for i in range(8):
        prog << Measure(i, i)

    counts = run_counts(prog, 1000)
    total = sum(counts.values())

    distribution = {}
    for key, count in counts.items():
        recovered = 0
        for index, bit in enumerate(key):
            if bit == "1":
                recovered |= 1 << pos_to_qubit[index]
        label = format(recovered, "08b")
        distribution[label] = distribution.get(label, 0.0) + count / total
    return distribution
