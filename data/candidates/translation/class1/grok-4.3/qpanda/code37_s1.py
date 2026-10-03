# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import init_quantum_machine, QMachineType, QProg, H, X, CNOT, Measure

def bv_algorithm(s):
    n = len(s)
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(n + 1)
    cbits = machine.cAlloc_many(n)
    prog = QProg()
    ancilla = n
    prog << X(qubits[ancilla])
    prog << [H(qb) for qb in qubits]
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(qubits[index], qubits[ancilla])
    for i in range(n):
        prog << H(qubits[i])
    for i in range(n):
        prog << Measure(qubits[i], cbits[i])
    result = machine.run_with_configuration(prog, cbits, shots=1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
