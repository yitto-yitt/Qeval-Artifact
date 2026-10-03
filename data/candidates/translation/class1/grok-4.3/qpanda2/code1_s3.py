# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def run_bell_state_simulator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1]) << pq.measure_all(qubits, cbits)
    counts = machine.run_with_configuration(prog, cbits, 1000)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
