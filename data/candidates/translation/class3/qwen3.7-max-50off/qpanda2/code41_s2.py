# EVAL_META: task_id=41, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def compose_op():
    return pq.PauliOperator("X0 Y2")

machine.finalize()
