# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def get_statevector(circuit):
    machine = pq.CPUQVM()
    machine.init_qvm()
    prog = pq.QProg()
    prog.insert(circuit)
    result = machine.prob_run_list(prog, [], -1)
    sv = machine.get_qstate()
    machine.finalize()
    return np.array(sv)
