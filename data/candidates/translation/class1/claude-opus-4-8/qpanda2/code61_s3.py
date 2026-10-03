# EVAL_META: task_id=61, framework=qpanda2, class=1
import pyqpanda as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    prog = pq.QProg()
    prog << pq.measure_all(q, c)
    result = machine.run_with_configuration(prog, c, 1024)
    machine.finalize()
    return result
