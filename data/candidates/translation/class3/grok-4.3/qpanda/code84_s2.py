# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import *
def controlled_custom_unitary_circuit():
    machine = QuantumMachine()
    q = machine.allocate_qubits(2)
    prog = Program()
    prog << CU(q[0], q[1], 0.3, 0.2, 0.1)
    return prog
