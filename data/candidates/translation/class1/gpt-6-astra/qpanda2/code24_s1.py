# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq


def dj_algorithm(oracle):
    oracle_prog = pq.QProg()
    oracle_prog << oracle

    try:
        used_qubits = oracle_prog.get_used_qubits()
    except TypeError:
        used_qubits = pq.QVec()
        oracle_prog.get_used_qubits(used_qubits)

    n = max(qubit.get_phy_addr() for qubit in used_qubits) + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(n)
        program = pq.QProg()
        program << pq.X(qubits[n - 1])

        for qubit in qubits:
            program << pq.H(qubit)

        program << oracle_prog

        for qubit in qubits:
            program << pq.H(qubit)

        probabilities = machine.prob_run_dict(program, qubits[:n - 1], -1)
        return {
            bitstring: float(probability)
            for bitstring, probability in probabilities.items()
            if probability > 1e-15
        }
    finally:
        machine.finalize()
