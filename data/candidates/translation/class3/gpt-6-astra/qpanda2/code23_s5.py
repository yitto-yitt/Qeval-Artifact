# EVAL_META: task_id=23, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def dj_constant_oracle():
    oracle = pq.QCircuit()
    oracle << pq.X(qubits[2])

    program = pq.QProg()
    program << oracle
    machine.directly_run(program)

    return oracle


atexit.register(machine.finalize)
