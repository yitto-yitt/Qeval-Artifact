# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq


def simons_algorithm(s):
    n = len(s)
    reversed_s = s[::-1]

    machine = pq.CPUQVM()
    machine.init_qvm()
    reg1 = machine.qAlloc_many(n)
    reg2 = machine.qAlloc_many(n)
    c = machine.cAlloc_many(n)

    program = pq.QProg()
    for qubit in reg1:
        program << pq.H(qubit)

    for control, target in zip(reg1, reg2):
        program << pq.CNOT(control, target)

    if "1" in reversed_s:
        i = reversed_s.find("1")
        for j in range(n):
            if reversed_s[j] == "1":
                program << pq.CNOT(reg1[i], reg2[j])
        for qubit in reg1:
            program << pq.H(qubit)

    for qubit, bit in zip(reg1, c):
        program << pq.Measure(qubit, bit)

    machine.directly_run(program)

    if not hasattr(simons_algorithm, "_machines"):
        simons_algorithm._machines = []
    simons_algorithm._machines.append(machine)
    return program
