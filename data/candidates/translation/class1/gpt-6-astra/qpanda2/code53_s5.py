# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(8)
        cbits = machine.cAlloc_many(8)
        program = pq.QProg()

        for value in (a, b):
            for i in range(8):
                if (value >> i) & 1:
                    program << pq.X(qubits[i])

        for i in range(8):
            program << pq.Measure(qubits[i], cbits[i])

        counts = machine.run_with_configuration(program, cbits, 1024)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
