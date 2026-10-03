# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def dj_algorithm(oracle):
    oracle_program = pq.QProg()
    oracle_program << oracle
    used_qubits = pq.get_all_used_qubits(oracle_program)
    addresses = [
        int(q.get_phy_addr()) if hasattr(q, "get_phy_addr") else int(q)
        for q in used_qubits
    ]
    n = builtins.max(addresses, default=0) + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(n)
        cbits = machine.cAlloc_many(n - 1)
        program = pq.QProg()
        program << pq.X(qubits[-1])
        for qubit in qubits:
            program << pq.H(qubit)
        program << oracle_program
        for qubit in qubits:
            program << pq.H(qubit)

        if not cbits:
            return dict(machine.prob_run_dict(program, qubits[:-1], -1))

        for qubit, cbit in zip(qubits[:-1], cbits):
            program << pq.Measure(qubit, cbit)

        counts = machine.run_with_configuration(program, cbits, 1024)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
