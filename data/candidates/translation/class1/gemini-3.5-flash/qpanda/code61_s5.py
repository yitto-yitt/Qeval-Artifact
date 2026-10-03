# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, Measure


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc()
    c = machine.cAlloc()
    prog = QProg()
    prog.insert(Measure(q, c))
    prog.machine = machine  # Keep machine alive
    return prog
