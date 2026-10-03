# EVAL_META: task_id=110, framework=qpanda, class=3
import random
from pyqpanda3.core import H, S, X, CNOT, CZ, SWAP

def equivalent_clifford_circuit(circuit, n):
    def _get_qubits(c):
        if hasattr(c, "get_qubits"):
            return list(c.get_qubits())
        if hasattr(c, "qubits"):
            return list(c.qubits())
        raise AttributeError("unable to obtain qubits")

    def _copy_container(c):
        out = type(c)()
        try:
            out << c
        except Exception:
            if hasattr(c, "get_gates"):
                for g in c.get_gates():
                    out << g
            else:
                raise
        return out

    qubits = _get_qubits(circuit)
    num_qubits = len(qubits)
    qc_list = []

    while len(qc_list) < n:
        qc = _copy_container(circuit)

        for _ in range(random.randint(1, 6)):
            idx = random.randrange(num_qubits)
            q = qubits[idx]
            max_type = 6 if num_qubits >= 2 else 3
            typ = random.randrange(max_type)

            if typ == 0:
                qc << H(q)
                qc << H(q)
            elif typ == 1:
                for _ in range(4):
                    qc << S(q)
            elif typ == 2:
                qc << X(q)
                qc << X(q)
            else:
                if num_qubits < 2:
                    for _ in range(4):
                        qc << S(q)
                    continue
                j = random.randrange(num_qubits)
                while j == idx:
                    j = random.randrange(num_qubits)
                q2 = qubits[j]
                if typ == 3:
                    qc << CNOT(q, q2)
                    qc << CNOT(q, q2)
                elif typ == 4:
                    qc << CZ(q, q2)
                    qc << CZ(q, q2)
                else:
                    qc << SWAP(q, q2)
                    qc << SWAP(q, q2)

        qc_list.append(qc)

    return qc_list
