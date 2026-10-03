# EVAL_META: task_id=61, framework=qpanda, class=1
import pyqpanda3.core as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = pq.QProg()
    measure_op = getattr(pq, "Measure", None)
    if measure_op is None:
        measure_op = getattr(pq, "measure")
    prog << measure_op(q[0], c[0])
    return prog
