# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import *


def not_gate(a):
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)

    prog = QProg()
    bitstring = format(a, "08b")
    for i in range(8):
        if bitstring[7 - i] == "0":
            prog << X(qubits[i])

    try:
        prog << measure_all(qubits, cbits)
    except NameError:
        for i in range(8):
            prog << Measure(qubits[i], cbits[i])

    shots = 1024
    if hasattr(machine, "run_with_configuration"):
        counts = machine.run_with_configuration(prog, cbits, shots)
    elif hasattr(machine, "run_with_config"):
        counts = machine.run_with_config(prog, cbits, shots)
    else:
        counts = machine.run(prog, cbits, shots)

    total = sum(counts.values())
    return {key[::-1] if len(key) == 8 else key: value / total for key, value in counts.items()}
