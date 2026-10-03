# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import init, finalize, QProg, QCircuit, Qubit, H, CNOT, Measure, QMachineFactory

def run_bell_state_simulator():
    init()
    vm = QMachineFactory.create_machine("CPU")
    vm.init()
    q = vm.qAlloc_many(2)
    c = vm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    result = vm.run_with_configuration(prog, [c[0], c[1]], 1000)
    counts = result
    total = sum(counts.values())
    finalize()
    return {key: value / total for key, value in counts.items()}
