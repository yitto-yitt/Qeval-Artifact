# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(256)

def equivalent_clifford_circuit(circuit, n):
    def _used_qubits(cir):
        used = []
        try:
            prog = QProg()
            prog << cir
            used = list(get_all_used_qubits(prog))
        except Exception:
            try:
                used = list(get_all_used_qubits(cir))
            except Exception:
                try:
                    used = list(cir.get_used_qubits())
                except Exception:
                    used = []
        normalized = []
        for qb in used:
            if hasattr(qb, "get_phy_addr"):
                normalized.append(qb)
            else:
                try:
                    normalized.append(q[int(qb)])
                except Exception:
                    pass
        return normalized

    def _add_random_identity(qc, qubits):
        if not qubits:
            return
        choice = random.randrange(6 if len(qubits) >= 2 else 5)
        qa = random.choice(qubits)
        if choice == 0:
            qc << H(qa) << H(qa)
        elif choice == 1:
            qc << X(qa) << X(qa)
        elif choice == 2:
            qc << Y(qa) << Y(qa)
        elif choice == 3:
            qc << Z(qa) << Z(qa)
        elif choice == 4:
            qc << S(qa) << S(qa) << S(qa) << S(qa)
        else:
            qb = random.choice(qubits)
            while qb == qa and len(qubits) > 1:
                qb = random.choice(qubits)
            qc << CNOT(qa, qb) << CNOT(qa, qb)

    qubits = _used_qubits(circuit)
    qc_list = []
    for _ in range(n):
        qc = QCircuit()
        for _ in range(random.randint(1, 4)):
            _add_random_identity(qc, qubits)
        qc << circuit
        for _ in range(random.randint(1, 4)):
            _add_random_identity(qc, qubits)
        qc_list.append(qc)
    return qc_list

atexit.register(machine.finalize)
