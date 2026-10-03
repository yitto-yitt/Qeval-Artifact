# EVAL_META: task_id=147, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def mcy(qc):
    qc << pq.Y(qubits[4]).control(qubits[:4])
    program = pq.QProg()
    program << qc
    machine.directly_run(program)
    return qc


atexit.register(lambda: machine.finalize())
