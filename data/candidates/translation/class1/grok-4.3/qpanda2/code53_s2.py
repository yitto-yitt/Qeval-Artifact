# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    prog = pq.QProg()
    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(qubits[i])
    for i in range(8):
        if (b >> i) & 1:
            prog << pq.X(qubits[i])
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])
    shots = 1024
    result = machine.run_with_configuration(prog, shots)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
