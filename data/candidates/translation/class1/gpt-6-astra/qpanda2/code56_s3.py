# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(8)
        cbits = machine.cAlloc_many(8)
        program = pq.QProg()
        a = format(a, "08b")
        for i in range(8):
            if a[7 - i] == "0":
                program << pq.X(qubits[i])
        for i in range(8):
            program << pq.Measure(qubits[i], cbits[i])
        counts = machine.run_with_configuration(program, cbits, 1024)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
