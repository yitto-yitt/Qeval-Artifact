# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq

def create_ghz(drawing=False):
    pq.init(pq.QMachineType.CPU)
    q = pq.qAlloc_many(3)
    c = pq.cAlloc_many(3)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.CNOT(q[0], q[2])
    prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1]) << pq.Measure(q[2], c[2])
    if drawing:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, '3-qubit GHZ state circuit', ha='center')
        ax.axis('off')
        return prog, fig
    return prog
