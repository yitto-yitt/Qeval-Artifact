# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def run_bell_state_simulator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.q_alloc_many(2)
    cbits = machine.c_alloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    prog << pq.measure(qubits[0], cbits[0]) << pq.measure(qubits[1], cbits[1])
    shots = 1000
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
