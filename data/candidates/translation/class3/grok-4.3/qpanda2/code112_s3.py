# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    q = qubits[:n]
    circuit = QCircuit()
    for pauli_str, time in zip(pauli_strings, times):
        dt = time / reps
        for _ in range(reps):
            active = [(i, pauli_str[i]) for i in range(n) if pauli_str[i] != 'I']
            if not active:
                continue
            target_idx, target_p = active[-1]
            target_q = q[target_idx]
            if target_p == 'X':
                circuit << H(target_q)
            elif target_p == 'Y':
                circuit << RX(target_q, np.pi / 2)
            for idx, p in active[:-1]:
                qq = q[idx]
                if p == 'X':
                    circuit << H(qq)
                elif p == 'Y':
                    circuit << RX(qq, np.pi / 2)
                circuit << CNOT(qq, target_q)
            circuit << RZ(target_q, 2 * dt)
            for idx, p in reversed(active[:-1]):
                qq = q[idx]
                circuit << CNOT(qq, target_q)
                if p == 'X':
                    circuit << H(qq)
                elif p == 'Y':
                    circuit << RX(qq, -np.pi / 2)
            if target_p == 'X':
                circuit << H(target_q)
            elif target_p == 'Y':
                circuit << RX(target_q, -np.pi / 2)
    return circuit
machine.finalize()
