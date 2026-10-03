# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    prog = pq.QProg()
    prog.insert(circuit)
    qvm.run(prog)
    state = qvm.get_qstate()
    qvm.finalize()
    return state
