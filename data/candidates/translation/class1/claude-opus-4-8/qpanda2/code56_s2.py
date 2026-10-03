# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    prog = pq.QProg()
    a = format(a, "08b")
    for i in range(8):
        if a[7 - i] == "0":
            prog << pq.X(qubits[i])
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    machine.finalize()
    total = shots
    return {key: value / total for key, value in counts.items()}
