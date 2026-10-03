# EVAL_META: task_id=36, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def bv_function(s):
    n = len(s)
    while len(qubits) < n + 1:
        qubits.append(machine.qAlloc())

    oracle = pq.QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            oracle << pq.CNOT(qubits[index], qubits[n])

    program = pq.QProg()
    program << oracle
    machine.directly_run(program)
    return oracle


atexit.register(lambda: machine.finalize())
