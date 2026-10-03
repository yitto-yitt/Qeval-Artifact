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
            for bit in range(8):
                if (value >> bit) & 1:
                    program << pq.X(qubits[bit])

        program << pq.measure_all(qubits, cbits)
        counts = machine.run_with_configuration(program, cbits, 1024)
        total = builtins.sum(counts.values())
        return {key: count / total for key, count in counts.items()}
    finally:
        machine.finalize()
