# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QMachineType, QProg, H, CNOT, Measure

def noisy_bell():
    machine = QuantumMachine(QMachineType.CPU)
    init_method = getattr(machine, "init_qvm", None) or getattr(machine, "init", None)
    init_method()

    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    counts = machine.run_with_configuration(prog, 1000)
    total = sum(counts.values())
    machine.finalize()

    return {key: value / total for key, value in counts.items()}
