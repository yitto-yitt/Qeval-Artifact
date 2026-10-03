# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, CNOT, Measure, CPUQVM

def bell_each_shot():
    prog = QProg()
    prog << H(0)
    prog << CNOT(0, 1)
    prog << Measure(0, 0)
    prog << Measure(1, 1)
    
    machine = CPUQVM()
    machine.init_qvm()
    counts = machine.run_with_configuration(prog, 10)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
