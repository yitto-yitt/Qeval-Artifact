# EVAL_META: task_id=27, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
cbits = machine.cAlloc_many(3)


def apply_op_back():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.H(qubits[0])

    machine.directly_run(prog)

    try:
        dag = pq.QProgDAG(prog)
    except TypeError:
        dag = pq.QProgDAG()
        dag.build_dag(prog)
    return dag


atexit.register(machine.finalize)
