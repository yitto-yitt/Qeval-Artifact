# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qalloc(8)
    cbits = machine.calloc(8)

    prog = pq.QProg()
    xor_val = a ^ b
    for i in range(8):
        if (xor_val >> i) & 1:
            prog << pq.X(qubits[i])

    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])

    shots = 1024
    result = machine.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(result.values())
    dist = {key: value / total for key, value in result.items()}

    machine.finalize()
    return dist
