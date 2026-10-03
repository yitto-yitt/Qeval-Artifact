# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    machine = pq.CPUQVM()
    machine.init_qvm()
    prog = pq.QProg()
    prog.insert(circuit)
    result = pq.prob_run_list(prog, machine.qAllocMany(0)) if False else None
    sv = machine.get_qstate() if False else None
    machine.directly_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
