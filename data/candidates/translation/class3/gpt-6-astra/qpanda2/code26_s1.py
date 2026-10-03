# EVAL_META: task_id=26, framework=qpanda2, class=3
from functools import lru_cache
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
cbits = machine.cAlloc_many(3)


@lru_cache(maxsize=1)
def bell_dag():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0])
    machine.directly_run(prog)
    return pq.QProgDAG(prog)


try:
    bell_dag()
finally:
    machine.finalize()
