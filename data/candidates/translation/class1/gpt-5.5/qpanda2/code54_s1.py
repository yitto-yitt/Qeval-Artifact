# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def and_gate(a, b):
    shots = 1024

    def _calibrate_positions():
        pos_for_cbit = {}
        for active in range(3):
            machine = init_quantum_machine(QMachineType.CPU)
            qs = machine.qAlloc_many(3)
            cs = machine.cAlloc_many(3)
            prog = QProg()
            prog << X(qs[active])
            for j in range(3):
                prog << Measure(qs[j], cs[j])
            counts = machine.run_with_configuration(prog, cs, 1)
            destroy_quantum_machine(machine)
            key = max(counts, key=counts.get)
            pos_for_cbit[active] = key.find("1")
        return pos_for_cbit

    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(3)

    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]

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
        prog << Measure(ancillary[i], cbits[i])

    counts = machine.run_with_configuration(prog, cbits, shots)
    destroy_quantum_machine(machine)

    pos_for_cbit = _calibrate_positions()

    reordered_counts = {}
    for key, value in counts.items():
        out_key = key[pos_for_cbit[2]] + key[pos_for_cbit[1]] + key[pos_for_cbit[0]]
        reordered_counts[out_key] = reordered_counts.get(out_key, 0) + value

    total = builtins.sum(reordered_counts.values())
    return {key: value / total for key, value in reordered_counts.items()}
