# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda import *
from numpy import isclose

def dj_algorithm(oracle):
    n = oracle.get_qubit_number()
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    cbits = machine.cAlloc_many(n - 1)
    prog = QProg()
    prog.insert(X(qubits[n - 1]))
    for i in range(n):
        prog.insert(H(qubits[i]))
    prog.insert(oracle)
    for i in range(n):
        prog.insert(H(qubits[i]))
    for i in range(n - 1):
        prog.insert(Measure(qubits[i], cbits[i]))
    result = machine.run_with_configuration(prog, cbits, 1024)
    machine.finalize()
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
