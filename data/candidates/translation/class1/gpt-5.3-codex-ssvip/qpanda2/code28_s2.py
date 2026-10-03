# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def visualize_bell_states():
    shots = 1000

    # phi_plus state
    machine1 = pq.init_quantum_machine(pq.QMachineType.CPU)
    q1 = machine1.qAlloc_many(2)
    c1 = machine1.cAlloc_many(2)

    prog1 = pq.QProg()
    prog1 << pq.H(q1[0]) << pq.CNOT(q1[0], q1[1])
    prog1 << pq.Measure(q1[0], c1[0]) << pq.Measure(q1[1], c1[1])

    phi_plus_counts = machine1.run_with_configuration(prog1, c1, shots)
    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_plus_probs = {k: v / phi_plus_total for k, v in phi_plus_counts.items()}

    pq.destroy_quantum_machine(machine1)

    # phi_minus state (as in reference: X on qubit 0, then H and CNOT)
    machine2 = pq.init_quantum_machine(pq.QMachineType.CPU)
    q2 = machine2.qAlloc_many(2)
    c2 = machine2.cAlloc_many(2)

    prog2 = pq.QProg()
    prog2 << pq.X(q2[0]) << pq.H(q2[0]) << pq.CNOT(q2[0], q2[1])
    prog2 << pq.Measure(q2[0], c2[0]) << pq.Measure(q2[1], c2[1])

    phi_minus_counts = machine2.run_with_configuration(prog2, c2, shots)
    phi_minus_total = builtins.sum(phi_minus_counts.values())
    phi_minus_probs = {k: v / phi_minus_total for k, v in phi_minus_counts.items()}

    pq.destroy_quantum_machine(machine2)

    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs,
    }
