# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def or_gate(a, b):
    """Bitwise OR of two 3-bit integers using a quantum circuit.

    Qubits 0-2 hold the bits of ``a``, qubits 3-5 hold the bits of ``b``
    and qubits 6-8 are the output register.  Each output qubit is prepared
    in |1> and then flipped by a Toffoli controlled on the corresponding
    pair of input qubits, yielding ``out_i = a_i OR b_i``.

    Returns a probability distribution dict keyed by 3-bit strings.
    """
    a = int(a) & 0b111
    b = int(b) & 0b111

    qc = QuantumCircuit(9, 3, name="or_gate")

    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)

        # out_i = NOT(a_i AND b_i) = a_i OR b_i
        qc.x(6 + i)
        qc.ccx(i, 3 + i, 6 + i)

    for i in range(3):
        qc.measure(6 + i, i)

    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
