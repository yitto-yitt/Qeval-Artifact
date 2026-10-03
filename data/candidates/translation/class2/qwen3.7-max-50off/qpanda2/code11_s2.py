# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    state = qvm.get_state(circuit)
    return state
