# EVAL_META: task_id=28, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def visualize_bell_states():
    shots = 1000

    # phi_plus: (|00> + |11>) / sqrt(2)
    machine1 = init_quantum_machine(QMachineType.CPU)
    q1 = machine1.qAlloc_many(2)
    c1 = machine1.cAlloc_many(2)
    prog1 = QProg()
    prog1 << H(q1[0]) << CNOT(q1[0], q1[1]) << Measure(q1[0], c1[0]) << Measure(q1[1], c1[1])
    counts1 = machine1.run_with_configuration(prog1, c1, shots)
    destroy_quantum_machine(machine1)

    # phi_minus equivalent circuit from reference: X(0) -> H(0) -> CNOT(0,1)
    machine2 = init_quantum_machine(QMachineType.CPU)
    q2 = machine2.qAlloc_many(2)
    c2 = machine2.cAlloc_many(2)
    prog2 = QProg()
    prog2 << X(q2[0]) << H(q2[0]) << CNOT(q2[0], q2[1]) << Measure(q2[0], c2[0]) << Measure(q2[1], c2[1])
    counts2 = machine2.run_with_configuration(prog2, c2, shots)
    destroy_quantum_machine(machine2)

    total1 = builtins.sum(counts1.values())
    total2 = builtins.sum(counts2.values())

    return {
        "phi_plus": {k: v / total1 for k, v in counts1.items()},
        "phi_minus": {k: v / total2 for k, v in counts2.items()},
    }
