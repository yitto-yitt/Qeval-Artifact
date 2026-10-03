# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, measure

def dj_algorithm(oracle):
    n = oracle.num_qubits

    qc = QCircuit(n)
    qc << X(n - 1)
    for i in range(n):
        qc << H(i)

    from qiskit import qasm2
    from pyqpanda3.intermediate_compiler import convert_qasm_string_to_qprog
    oracle_qasm = qasm2.dumps(oracle)
    oracle_prog = convert_qasm_string_to_qprog(oracle_qasm)
    qc << oracle_prog

    for i in range(n):
        qc << H(i)

    prog = QProg()
    prog << qc
    for i in range(n - 1):
        prog << measure(i, i)

    qvm = CPUQVM()
    qvm.run(prog, 4096)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
