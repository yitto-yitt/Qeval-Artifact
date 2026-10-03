# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, Measure


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    program = QProg()
    program << Measure(q[0], c[0])
    machine.directly_run(program)

    function = create_quantum_circuit_with_one_qubit_and_measure
    if not hasattr(function, "_machines"):
        function._machines = []
    function._machines.append(machine)

    return program
