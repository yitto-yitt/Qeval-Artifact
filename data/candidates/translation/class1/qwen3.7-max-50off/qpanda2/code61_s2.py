# EVAL_META: task_id=61, framework=qpanda2, class=1
import pyqpanda as pq

def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qalloc(1)
    c = qvm.calloc(1)
    prog = pq.QProg()
    prog.measure(q[0], c[0])
    return prog
