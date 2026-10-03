# EVAL_META: task_id=89, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_controlled_hgate():
    prog = pq.QProg()
    ctrl_qubits = pq.QVec()
    ctrl_qubits.append(q[0])
    ctrl_qubits.append(q[1])
    gate = pq.H(q[2]).control(ctrl_qubits)
    prog.insert(gate)
    return prog

machine.finalize()
