# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import *

def or_gate(a, b):
    machine = CPUQVM()
    for name in ("init_qvm", "init", "initQVM"):
        if hasattr(machine, name):
            try:
                getattr(machine, name)()
            except TypeError:
                pass
            break

    def alloc_qubits(n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        return [machine.qAlloc() for _ in range(n)]

    qubits = alloc_qubits(9)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]

    prog = QProg()

    def append(op):
        try:
            prog << op
        except Exception:
            prog.insert(op)

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "0":
            append(X(qr_a[i]))
        if b_bits[2 - i] == "0":
            append(X(qr_b[i]))

    toffoli_gate = globals().get("Toffoli", globals().get("CCX"))
    for i in range(3):
        append(toffoli_gate(qr_a[i], qr_b[i], ancillary[i]))

    for i in range(3):
        append(X(ancillary[i]))

    def prob_run_one(q):
        if hasattr(machine, "prob_run_dict"):
            try:
                return machine.prob_run_dict(prog, [q], -1)
            except TypeError:
                try:
                    return machine.prob_run_dict(prog, [q])
                except TypeError:
                    return machine.prob_run_dict(prog, [q], 1)
        if hasattr(machine, "get_prob_dict"):
            if hasattr(machine, "directly_run"):
                machine.directly_run(prog)
            elif hasattr(machine, "run"):
                machine.run(prog)
            try:
                return machine.get_prob_dict([q], -1)
            except TypeError:
                return machine.get_prob_dict([q])
        raise RuntimeError("No probability execution API available")

    out_bits_lsb = []
    for q in ancillary:
        probs = prob_run_one(q)
        p1 = 0.0
        for key, value in probs.items():
            if isinstance(key, int):
                bit = str(key)
            elif isinstance(key, (list, tuple)):
                bit = "".join(str(x) for x in key)
            else:
                bit = str(key)
            if bit[-1] == "1":
                p1 += float(value)
        out_bits_lsb.append("1" if p1 > 0.5 else "0")

    key = out_bits_lsb[2] + out_bits_lsb[1] + out_bits_lsb[0]
    return {key: 1.0}
