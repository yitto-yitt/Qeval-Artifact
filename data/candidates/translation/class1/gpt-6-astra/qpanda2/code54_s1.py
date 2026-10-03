# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(9)
        cbits = machine.cAlloc_many(3)
        program = pq.QProg()
        a = format(a, '03b')
        b = format(b, '03b')
        for i in range(3):
            if a[2 - i] == '1':
                program << pq.X(qubits[i])
            if b[2 - i] == '1':
                program << pq.X(qubits[3 + i])
        for i in range(3):
            program << pq.Toffoli(qubits[i], qubits[3 + i], qubits[6 + i])
        for i in range(3):
            program << pq.Measure(qubits[6 + i], cbits[i])
        counts = machine.run_with_configuration(program, cbits, 1024)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
