# EVAL_META: task_id=56, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def not_gate(a):
    def run_x_indices(indices, shot_count):
        machine = init_quantum_machine(QMachineType.CPU)
        try:
            qubits = machine.qAlloc_many(8)
            cbits = machine.cAlloc_many(8)
            prog = QProg()
            for idx in indices:
                prog.insert(X(qubits[idx]))
            for idx in range(8):
                prog.insert(Measure(qubits[idx], cbits[idx]))
            return machine.run_with_configuration(prog, cbits, shot_count)
        finally:
            destroy_quantum_machine(machine)

    positions = [0] * 8
    for j in range(8):
        cal_counts = run_x_indices([j], 1)
        cal_key = max(cal_counts, key=cal_counts.get)
        cal_key = "".join(ch for ch in cal_key if ch in "01")
        positions[j] = cal_key.index("1")

    bit_string = format(a, "08b")
    x_indices = [i for i in range(8) if bit_string[7 - i] == "0"]
    counts = run_x_indices(x_indices, 1024)

    converted_counts = {}
    for raw_key, value in counts.items():
        raw_key = "".join(ch for ch in raw_key if ch in "01")
        out = ["0"] * 8
        for j in range(8):
            out[7 - j] = raw_key[positions[j]]
        key = "".join(out)
        converted_counts[key] = converted_counts.get(key, 0) + value

    total = builtins.sum(converted_counts.values())
    return {key: value / total for key, value in converted_counts.items()}
