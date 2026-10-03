# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.CNOT(q[0], q[2]))
    prog.insert(pq.Measure(q[0], c[0]))
    prog.insert(pq.Measure(q[1], c[1]))
    prog.insert(pq.Measure(q[2], c[2]))

    if drawing:
        try:
            draw_obj = pq.draw_qprog(prog, output="pic")
        except Exception:
            draw_obj = pq.draw_qprog(prog)
        return prog, draw_obj
    return prog
