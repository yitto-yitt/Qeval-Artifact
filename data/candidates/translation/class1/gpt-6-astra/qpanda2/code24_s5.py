# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq

def dj_algorithm(oracle):
    oracle_program = pq.QProg()
    oracle_program << oracle
    used_qubits = pq.QVec()
    oracle_program.get_used_qubits(used_qubits)
    n = max(qubit.get_phy_addr() for qubit in used_qubits) + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(n)
        cbits = machine.cAlloc_many(n - 1)
        program = pq.QProg()
        program << pq.X(qubits[n - 1])
        for qubit in qubits:
            program << pq.H(qubit)
        program << oracle_program
        for qubit in qubits:
            program << pq.H(qubit)
        for index in range(n - 1):
            program << pq.Measure(qubits[index], cbits[index])

        shots = 1024
        counts = machine.run_with_configuration(program, cbits, shots)
        return {key: value / shots for key, value in counts.items()}
    finally:
        machine.finalize()
