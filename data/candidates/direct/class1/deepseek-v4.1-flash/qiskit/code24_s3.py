# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def dj_algorithm(oracle):
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1)
    qc.h(range(n))
    qc.x(n)
    qc.h(n)
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    sv = Statevector.from_instruction(qc)
    probs = {}
    for i, amp in enumerate(sv.data):
        input_val = i & ((1 << n) - 1)
        key = format(input_val, f'0{n}b')
        probs[key] = probs.get(key, 0.0) + abs(amp) ** 2
    return probs
