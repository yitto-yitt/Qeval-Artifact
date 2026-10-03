# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def bv_algorithm(s):
    n = len(s)
    q = QuantumRegister(n + 1, "q")
    meas = ClassicalRegister(n, "meas")
    qc = QuantumCircuit(q, meas)
    ancilla = n

    qc.x(q[ancilla])
    qc.h(q)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(q[index], q[ancilla])
    qc.h(q[:n])
    qc.measure(q[:n], meas)

    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result = sampler.run([qc], shots=1).result()
    bitstrings = result[0].data.meas.get_bitstrings()
    return [bitstrings, result]

