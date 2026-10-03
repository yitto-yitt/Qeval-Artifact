# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def bell_each_shot():
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        cbits = machine.cAlloc_many(2)
        program = pq.QProg()
        program << pq.H(qubits[0])
        program << pq.CNOT(qubits[0], qubits[1])
        program << pq.Measure(qubits[0], cbits[0])
        program << pq.Measure(qubits[1], cbits[1])
        counts = machine.run_with_configuration(program, cbits, 10)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
