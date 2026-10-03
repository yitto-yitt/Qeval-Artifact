# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.CNOT(qubits[0], qubits[2]) \
         << pq.Measure(qubits[0], cbits[0]) \
         << pq.Measure(qubits[1], cbits[1]) \
         << pq.Measure(qubits[2], cbits[2])

    if drawing:
        try:
            draw_out = pq.draw_qprog(prog, "text")
        except:
            draw_out = pq.draw_qprog(prog)
        return prog, draw_out
    return prog
