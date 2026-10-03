# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import *
from math import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    marker_pattern = "1011001110001010"
    marker_count = len(marker_pattern)

    machine = CPUQVM()
    if hasattr(machine, "init"):
        machine.init()
    elif hasattr(machine, "init_qvm"):
        machine.init_qvm()

    total_qubits = 1 + marker_count
    if hasattr(machine, "qAlloc_many"):
        q = machine.qAlloc_many(total_qubits)
    elif hasattr(machine, "qalloc_many"):
        q = machine.qalloc_many(total_qubits)
    else:
        q = machine.qAllocMany(total_qubits)

    if hasattr(machine, "cAlloc_many"):
        c = machine.cAlloc_many(measurements + marker_count)
    elif hasattr(machine, "calloc_many"):
        c = machine.calloc_many(measurements + marker_count)
    else:
        c = machine.cAllocMany(measurements + marker_count)

    q = list(q)
    c = list(c)

    prog = QProg()

    def add(node):
        nonlocal prog
        try:
            prog << node
        except Exception:
            prog.insert(node)

    for i in range(cycles):
        add(RY(q[0], e))
        if bomb_live:
            add(Measure(q[0], c[i]))

    add(Measure(q[0], c[measurements - 1]))

    for j, bit in enumerate(marker_pattern):
        if bit == "1":
            add(X(q[1 + j]))
        add(Measure(q[1 + j], c[measurements + j]))

    if hasattr(machine, "run_with_configuration"):
        try:
            counts = machine.run_with_configuration(prog, c, shots)
        except TypeError:
            counts = machine.run_with_configuration(prog, shots, c)
    else:
        counts = machine.run(prog, c, shots)

    if hasattr(counts, "get_counts"):
        counts = counts.get_counts()
    elif hasattr(counts, "result") and callable(counts.result):
        counts = counts.result()

    live_predictions = 0.0
    dud_predictions = 0.0
    detonations = 0.0

    def algorithm_bits(raw_key):
        s = "".join(ch for ch in str(raw_key) if ch in "01")
        m = measurements
        k = marker_count
        if len(s) >= m + k:
            if s[-k:] == marker_pattern:
                return s[:m]
            if s[:k] == marker_pattern[::-1]:
                return s[k:k + m][::-1]
            pos = s.find(marker_pattern)
            if pos >= 0 and pos >= m:
                return s[pos - m:pos]
            pos = s.find(marker_pattern[::-1])
            if pos == 0:
                return s[k:k + m][::-1]
        if len(s) >= m:
            return s[:m]
        return s

    total_weight = 0.0
    items = counts.items() if hasattr(counts, "items") else dict(counts).items()

    for key, value in items:
        weight = float(value)
        total_weight += weight
        bits = algorithm_bits(key)
        if bomb_live:
            if bits and bits[measurements - 1] == "1":
                detonations += weight
            elif "1" in bits[:measurements - 1]:
                dud_predictions += weight
            else:
                live_predictions += weight
        else:
            if bits and bits[0] == "0":
                live_predictions += weight
            else:
                dud_predictions += weight

    denom = 1.0 if 0.0 < total_weight <= 1.0000001 else float(shots)

    if hasattr(machine, "finalize"):
        machine.finalize()
    elif hasattr(machine, "finalize_qvm"):
        machine.finalize_qvm()

    return {
        "live_predictions": live_predictions / denom,
        "dud_predictions": dud_predictions / denom,
        "detonations": detonations / denom,
    }
