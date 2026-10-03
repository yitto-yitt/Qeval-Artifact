# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def apply_op_back():
    dag = QCircuit()
    dag << H(q[0])
    dag << CNOT(q[0], q[1])
    dag << H(q[0])
    return dag

machine.finalize()
