# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(9)
        measure = machine.cAlloc_many(3)
        qr_a = qubits[:3]
        qr_b = qubits[3:6]
        ancillary = qubits[6:]
        program = pq.QProg()
        a = format(a, "03b")
        b = format(b, "03b")

        for i in range(3):
            if a[2 - i] == "0":
                program << pq.X(qr_a[i])
            if b[2 - i] == "0":
                program << pq.X(qr_b[i])

        for i in range(3):
            program << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])

        for i in range(3):
            program << pq.X(ancillary[i])

        for i in range(3):
            program << pq.Measure(ancillary[i], measure[i])

        counts = machine.run_with_configuration(program, measure, 1024)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
