# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(20)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    q = qubits[:n]
    circuit = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            active = [(i, pauli_string[i]) for i in range(n) if pauli_string[i] != 'I']
            if not active:
                continue
            for i, p in active:
                if p == 'X':
                    circuit << H(q[i])
                elif p == 'Y':
                    circuit << Sdag(q[i]) << H(q[i])
            active_qubits = [q[i] for i, p in active]
            k = len(active_qubits)
            if k > 1:
                for i in range(k - 1):
                    circuit << CNOT(active_qubits[i], active_qubits[i + 1])
            circuit << RZ(active_qubits[-1], 2 * time / reps)
            if k > 1:
                for i in reversed(range(k - 1)):
                    circuit << CNOT(active_qubits[i], active_qubits[i + 1])
            for i, p in reversed(active):
                if p == 'X':
                    circuit << H(q[i])
                elif p == 'Y':
                    circuit << H(q[i]) << S(q[i])
    return circuit

machine.finalize()
