# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, X, H, CNOT, Measure
def bv_algorithm(s):
    n = len(s)
    machine = QuantumMachine()
    q = machine.allocate_qubits(n + 1)
    c = machine.allocate_cbits(n)
    prog = QProg()
    ancilla = n
    prog.insert(X(q[ancilla]))
    for qubit in q:
        prog.insert(H(qubit))
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog.insert(CNOT(q[index], q[ancilla]))
    for i in range(n):
        prog.insert(H(q[i]))
    for i in range(n):
        prog.insert(Measure(q[i], c[i]))
    result = machine.run_with_configuration(prog, shots=1)
    bitstrings = list(result.keys()) if isinstance(result, dict) else []
    return [bitstrings, result]
