# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, measure
from qiskit import QuantumCircuit


def _qiskit_oracle_to_qpanda(oracle, qubits):
    n = oracle.num_qubits
    circ = QCircuit()
    for instr in oracle.data:
        op = instr.operation
        name = op.name.lower()
        qargs = [oracle.find_bit(q).index for q in instr.qubits]
        if name in ('id', 'i', 'barrier'):
            continue
        elif name == 'x':
            circ << X(qubits[qargs[0]])
        elif name == 'h':
            circ << H(qubits[qargs[0]])
        elif name == 'cx':
            circ << X(qubits[qargs[1]]).control(qubits[qargs[0]])
        elif name == 'ccx':
            circ << X(qubits[qargs[2]]).control([qubits[qargs[0]], qubits[qargs[1]]])
        elif name == 'cz':
            from pyqpanda3.core import Z
            circ << Z(qubits[qargs[1]]).control(qubits[qargs[0]])
        elif name == 'z':
            from pyqpanda3.core import Z
            circ << Z(qubits[qargs[0]])
        elif name == 'mcx':
            ctrls = [qubits[q] for q in qargs[:-1]]
            circ << X(qubits[qargs[-1]]).control(ctrls)
        else:
            mat = op.to_matrix()
            from pyqpanda3.core import matrix_decompose
            sub = QCircuit()
            tmp_qs = [qubits[q] for q in qargs]
            from pyqpanda3.core import U4
            raise NotImplementedError("Unsupported gate: " + name)
    return circ


def dj_algorithm(oracle):
    n = oracle.num_qubits
    qubits = list(range(n))

    circ = QCircuit()
    circ << X(qubits[n - 1])
    for q in qubits:
        circ << H(qubits[q])

    circ << _qiskit_oracle_to_qpanda(oracle, qubits)

    for q in qubits:
        circ << H(qubits[q])

    prog = QProg()
    prog << circ
    for i in range(n - 1):
        prog << measure(qubits[i], i)

    qvm = CPUQVM()
    qvm.run(prog, 4096)
    raw = qvm.result().get_counts()

    counts = {}
    for key, value in raw.items():
        trimmed = key[-(n - 1):] if len(key) >= (n - 1) else key.zfill(n - 1)
        counts[trimmed] = counts.get(trimmed, 0) + value

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
