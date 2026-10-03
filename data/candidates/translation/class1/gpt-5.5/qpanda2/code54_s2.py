# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def and_gate(a, b):
    a = format(a, '03b')
    b = format(b, '03b')
    shots = 1024
    measured_bits = []

    for out_i in range(3):
        qvm = pq.CPUQVM()
        qvm.init_qvm()
        try:
            q = qvm.qAlloc_many(9)
            c = qvm.cAlloc_many(1)
            prog = pq.QProg()

            for i in range(3):
                if a[2 - i] == '1':
                    prog << pq.X(q[i])
                if b[2 - i] == '1':
                    prog << pq.X(q[3 + i])

            for i in range(3):
                prog << pq.Toffoli(q[i], q[3 + i], q[6 + i])

            prog << pq.Measure(q[6 + out_i], c[0])

            counts = qvm.run_with_configuration(prog, c, shots)
            total = builtins.sum(counts.values())
            p1 = counts.get('1', 0) / total if total else 0.0
            measured_bits.append('1' if p1 >= 0.5 else '0')
        finally:
            qvm.finalize()

    key = measured_bits[2] + measured_bits[1] + measured_bits[0]
    return {key: 1.0}
