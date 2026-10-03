# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq
import atexit

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    prog = pq.QProg()
    prog << pq.X(q[0])
    
    control_qubits = pq.QVec()
    control_qubits.append(q[1])
    cry_gate = pq.RY(q[2], 0.2).control(control_qubits)
    prog << cry_gate
    return prog

atexit.register(machine.finalize)
