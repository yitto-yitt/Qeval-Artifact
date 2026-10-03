# EVAL_META: task_id=56, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def not_gate(a):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    prog = QProg()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7 - i] == "0":
            prog.insert(X(qubits[i]))
    prog.insert(measure_all(qubits, cbits))
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
