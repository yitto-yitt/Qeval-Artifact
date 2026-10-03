# EVAL_META: task_id=118, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_c3sx_circuit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(4)
    prog = pq.QProg()
    
    ctrls = pq.QVec()
    ctrls.append(q[0])
    ctrls.append(q[1])
    ctrls.append(q[2])
    
    gate = pq.SX(q[3]).control(ctrls)
    prog.insert(gate)
    return prog
