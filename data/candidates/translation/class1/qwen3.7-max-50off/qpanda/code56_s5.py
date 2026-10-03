# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def not_gate(a):
    qc = QuantumCircuit(8)
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            qc.x(i)
    qc.measure_all()
    machine = QMachine()
    counts = machine.run(qc, 1000)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
