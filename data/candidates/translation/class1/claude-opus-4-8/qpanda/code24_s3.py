# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, measure

def dj_algorithm(oracle):
    n = oracle.num_qubits

    qc = QCircuit(n)
    qc << X(n - 1)
    for i in range(n):
        qc << H(i)

    from qiskit import QuantumCircuit
    from qiskit.qasm2 import dumps
    oracle_qc = QuantumCircuit(n)
    oracle_qc.compose(oracle, inplace=True)

    oracle_circ = QCircuit(n)
    for instr in oracle_qc.data:
        name = instr.operation.name
        qubits = [oracle_qc.find_bit(q).index for q in instr.qubits]
        if name == "x":
            oracle_circ << X(qubits[0])
        elif name == "h":
            oracle_circ << H(qubits[0])
        elif name == "cx":
            from pyqpanda3.core import CNOT
            oracle_circ << CNOT(qubits[0], qubits[1])
        elif name == "cz":
            from pyqpanda3.core import CZ
            oracle_circ << CZ(qubits[0], qubits[1])
        elif name == "z":
            from pyqpanda3.core import Z
            oracle_circ << Z(qubits[0])
        elif name == "ccx":
            from pyqpanda3.core import Toffoli
            oracle_circ << Toffoli(qubits[0], qubits[1], qubits[2])
        elif name in ("id", "barrier"):
            continue
        else:
            raise ValueError(f"Unsupported gate: {name}")

    qc << oracle_circ
    for i in range(n):
        qc << H(i)

    prog = QProg()
    prog << qc
    for i in range(n - 1):
        prog << measure(i, i)

    qvm = CPUQVM()
    qvm.run(prog, 4096)
    result = qvm.result().get_counts()

    total = sum(result.values())
    dist = {}
    for key, value in result.items():
        bitstr = key[-(n - 1):] if n - 1 > 0 else ""
        dist[bitstr] = dist.get(bitstr, 0) + value / total
    return dist
