# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure, measure_all
def noisy_bell():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog = measure_all(prog, q, c)
    result = machine.run_with_configuration(prog, cbit_list=c, shots=1000)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
