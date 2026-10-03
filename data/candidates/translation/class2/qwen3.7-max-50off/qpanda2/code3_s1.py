# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq

def create_ghz(drawing=False):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.CNOT(q[0], q[2])
    
    for i in range(3):
        prog << pq.Measure(q[i], c[i])
        
    if drawing:
        try:
            fig = pq.draw_qprog(prog, backend='mpl')
        except TypeError:
            fig = pq.draw_qprog(prog)
        return prog, fig
    return prog
