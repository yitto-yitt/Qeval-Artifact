# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq


def simons_algorithm(s):
    global _simons_algorithm_qvm
    n = len(s)
    s = s[::-1]

    _simons_algorithm_qvm = pq.CPUQVM()
    _simons_algorithm_qvm.init_qvm()

    q_reg1 = _simons_algorithm_qvm.qAlloc_many(n)
    q_reg2 = _simons_algorithm_qvm.qAlloc_many(n)
    c_reg = _simons_algorithm_qvm.cAlloc_many(n)

    circuit = pq.QProg()

    for i in range(n):
        circuit << pq.H(q_reg1[i])

    for i in range(n):
        circuit << pq.CNOT(q_reg1[i], q_reg2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << pq.CNOT(q_reg1[i], q_reg2[j])
        for j in range(n):
            circuit << pq.H(q_reg1[j])

    for i in range(n):
        circuit << pq.Measure(q_reg1[i], c_reg[i])

    return circuit
