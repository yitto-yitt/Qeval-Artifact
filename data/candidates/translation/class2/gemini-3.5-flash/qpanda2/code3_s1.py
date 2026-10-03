# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq

_machines = []

def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    _machines.append(machine)
    
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) \
         << pq.CNOT(q[0], q[1]) \
         << pq.CNOT(q[0], q[2])
         
    prog << pq.Measure(q[0], c[0]) \
         << pq.Measure(q[1], c[1]) \
         << pq.Measure(q[2], c[2])
         
    if drawing:
        try:
            pic = pq.draw_qprog(prog)
        except Exception:
            pic = ""
        return prog, pic
    return prog
