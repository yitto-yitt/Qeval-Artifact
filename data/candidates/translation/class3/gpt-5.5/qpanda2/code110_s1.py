# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qv = machine.qAlloc_many(32)

def equivalent_clifford_circuit(circuit, n):
    def get_qubits_from_circuit(cir):
        qubits = []
        try:
            qubits = list(cir.get_used_qubits())
        except Exception:
            qubits = []
        if not qubits:
            try:
                num_qubits = int(cir.num_qubits)
                qubits = list(qv[:num_qubits])
            except Exception:
                qubits = []
        try:
            qubits = sorted(qubits, key=lambda qb: qb.get_phy_addr())
        except Exception:
            pass
        return qubits

    def make_gate(desc, qubits):
        name = desc[0]
        if name == "H":
            return H(qubits[desc[1]])
        if name == "X":
            return X(qubits[desc[1]])
        if name == "Y":
            return Y(qubits[desc[1]])
        if name == "Z":
            return Z(qubits[desc[1]])
        if name == "CNOT":
            return CNOT(qubits[desc[1]], qubits[desc[2]])
        if name == "CZ":
            return CZ(qubits[desc[1]], qubits[desc[2]])
        if name == "SWAP":
            return SWAP(qubits[desc[1]], qubits[desc[2]])
        return H(qubits[desc[1]])

    def random_self_inverse_clifford_descriptors(num_qubits):
        if num_qubits <= 0:
            return []
        one_qubit_gates = ["H", "X", "Y", "Z"]
        two_qubit_gates = ["CNOT", "CZ", "SWAP"]
        depth = random.randint(1, max(1, 2 * num_qubits + 3))
        descs = []
        for _ in range(depth):
            if num_qubits >= 2 and random.random() < 0.45:
                gate_name = random.choice(two_qubit_gates)
                a, b = random.sample(range(num_qubits), 2)
                descs.append((gate_name, a, b))
            else:
                gate_name = random.choice(one_qubit_gates)
                a = random.randrange(num_qubits)
                descs.append((gate_name, a))
        return descs

    def insert_identity_from_descriptors(qc, descs, qubits):
        for desc in descs:
            qc.insert(make_gate(desc, qubits))
        for desc in reversed(descs):
            qc.insert(make_gate(desc, qubits))

    qubits = get_qubits_from_circuit(circuit)
    num_qubits = len(qubits)
    qc_list = []
    counter = 0

    while counter < n:
        qc = QCircuit()
        left_descs = random_self_inverse_clifford_descriptors(num_qubits)
        right_descs = random_self_inverse_clifford_descriptors(num_qubits)

        insert_identity_from_descriptors(qc, left_descs, qubits)
        qc.insert(circuit)
        insert_identity_from_descriptors(qc, right_descs, qubits)

        qc_list.append(qc)
        counter += 1

    return qc_list

atexit.register(machine.finalize)
