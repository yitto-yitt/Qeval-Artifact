# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def bell_each_shot():
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        q = machine.qAlloc_many(2)
        c = machine.cAlloc_many(2)

        prog = pq.QProg()
        prog << pq.H(q[0])
        prog << pq.CNOT(q[0], q[1])
        prog << pq.Measure(q[0], c[0])
        prog << pq.Measure(q[1], c[1])

        shots = 10
        counts = machine.run_with_configuration(prog, c, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
