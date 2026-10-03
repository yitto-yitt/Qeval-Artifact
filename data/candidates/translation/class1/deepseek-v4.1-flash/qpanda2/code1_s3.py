# EVAL_META: task_id=1, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def run_bell_state_simulator():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << measure_all(q, c)
    shots = 1000
    result = run_with_configuration(prog, c, shots)
    total = builtins.sum(result.values())
    machine.finalize()
    return {key: value / total for key, value in result.items()}
