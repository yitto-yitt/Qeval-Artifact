# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq


def and_gate(a, b):
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(9)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(9)
    elif hasattr(machine, "allocate_qubits"):
        qubits = machine.allocate_qubits(9)
    else:
        qubits = [machine.qAlloc() for _ in range(9)]

    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]

    prog = pq.QProg()

    def add(op):
        try:
            prog << op
        except Exception:
            prog.insert(op)

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "1":
            add(pq.X(qr_a[i]))
        if b_bits[2 - i] == "1":
            add(pq.X(qr_b[i]))

    for i in range(3):
        try:
            gate = pq.X(ancillary[i]).control([qr_a[i], qr_b[i]])
        except Exception:
            gate = pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])
        add(gate)

    measured_qubits = [ancillary[2], ancillary[1], ancillary[0]]

    if hasattr(machine, "prob_run_dict"):
        try:
            probs = machine.prob_run_dict(prog, measured_qubits, -1)
        except TypeError:
            probs = machine.prob_run_dict(prog, measured_qubits)
    elif hasattr(machine, "directly_run") and hasattr(machine, "get_prob_dict"):
        machine.directly_run(prog)
        probs = machine.get_prob_dict(measured_qubits)
    else:
        if hasattr(machine, "cAlloc_many"):
            cbits = machine.cAlloc_many(3)
        elif hasattr(machine, "calloc_many"):
            cbits = machine.calloc_many(3)
        else:
            cbits = [machine.cAlloc() for _ in range(3)]
        for i, q in enumerate(measured_qubits):
            add(pq.Measure(q, cbits[i]))
        counts = machine.run_with_configuration(prog, cbits, 1000)
        total = sum(counts.values())
        return {str(k).zfill(3): v / total for k, v in counts.items()}

    result = {}
    for key, value in probs.items():
        if isinstance(key, int):
            bitstr = format(key, "03b")
        else:
            bitstr = str(key).replace(" ", "")
            if len(bitstr) < 3:
                bitstr = bitstr.zfill(3)
            elif len(bitstr) > 3:
                bitstr = bitstr[-3:]
        p = float(value)
        if p > 1e-12:
            result[bitstr] = p

    total = sum(result.values())
    if total != 0:
        result = {k: v / total for k, v in result.items()}
    return result
