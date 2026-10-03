# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])

    state = machine.get_qstate()
    machine.finalize()

    probabilities = {}
    for i, amp in enumerate(state):
        p = (amp.real * amp.real + amp.imag * amp.imag)
        if p > 0:
            probabilities[format(i, "02b")] = p

    return probabilities
