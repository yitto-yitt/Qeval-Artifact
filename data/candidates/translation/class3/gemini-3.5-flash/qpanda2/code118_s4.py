# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = QProg()
    controls = QVec()
    controls.append(q[0])
    controls.append(q[1])
    controls.append(q[2])
    gate = SqiX(q[3]).control(controls)
    prog.insert(gate)
    return prog

# Manual Cleanup
machine.finalize()
