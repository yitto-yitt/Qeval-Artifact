# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *

# Initialize CPUQVM and qAlloc_many at the global scope
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = QProg()
    gate = SX(q[3])
    controlled_gate = gate.control([q[0], q[1], q[2]])
    prog.insert(controlled_gate)
    return prog

if __name__ == '__main__':
    machine.finalize()
