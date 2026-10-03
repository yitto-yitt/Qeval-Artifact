# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def dj_algorithm(oracle):
    oracle_prog = pq.QProg()
    oracle_prog << oracle
    used_qubits = oracle_prog.get_used_qubits()
    n = max(q.get_phy_addr() for q in used_qubits) + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(n)
        cbits = machine.cAlloc_many(n - 1)

        prog = pq.QProg()
        prog << pq.X(qubits[n - 1])
        for qubit in qubits:
            prog << pq.H(qubit)
        prog << oracle_prog
        for qubit in qubits:
            prog << pq.H(qubit)
        for i in range(n - 1):
            prog << pq.Measure(qubits[i], cbits[i])

        counts = machine.run_with_configuration(prog, cbits, 1024)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
