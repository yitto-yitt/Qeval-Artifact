# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def initialize_adjoint_and_compose(data1, data2):
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    machine.directly_run(prog)
    return data1, data1, data2
machine.finalize()
