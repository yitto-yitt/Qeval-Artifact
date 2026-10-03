# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq

def xor_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        q = machine.qAlloc_many(8)
        c = machine.cAlloc_many(8)

        prog = pq.QProg()

        x = a ^ b
        for i in range(8):
            if (x >> i) & 1:
                prog << pq.X(q[i])

        prog << pq.measure_all(q, c)

        shots = 1024
        counts = machine.run_with_configuration(prog, c, shots)
        return {k: v / shots for k, v in counts.items()}
    finally:
        pq.destroy_quantum_machine(machine)
