# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import QProg, QuantumMachine, QMachineType, H, CNOT, Measure

def bell_each_shot():
    machine = QuantumMachine(QMachineType.CPU)
    machine.init()
    q = machine.allocate_qubits(2)
    c = machine.allocate_classical_bits(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    counts = machine.run_with_configuration(prog, 10)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
