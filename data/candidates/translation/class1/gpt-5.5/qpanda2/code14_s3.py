# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def bell_each_shot():
    shots = 10

    machine = pq.CPUQVM()
    machine.init_qvm()

    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1]) << pq.measure_all(qubits, cbits)

    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())

    machine.finalize()

    return {key: value / total for key, value in counts.items()}
