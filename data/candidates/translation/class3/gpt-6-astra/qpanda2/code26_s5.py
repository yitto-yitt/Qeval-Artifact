# EVAL_META: task_id=26, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
cbits = machine.cAlloc_many(3)


def bell_dag():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0])
    dag = pq.QProgDAG(prog)
    machine.directly_run(prog)
    return dag


atexit.register(machine.finalize)
