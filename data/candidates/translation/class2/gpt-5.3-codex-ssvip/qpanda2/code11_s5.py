# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq


def get_statevector(circuit):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        qprog = pq.QProg()
        qprog << circuit
        return qvm.get_qstate()
    finally:
        qvm.finalize()
