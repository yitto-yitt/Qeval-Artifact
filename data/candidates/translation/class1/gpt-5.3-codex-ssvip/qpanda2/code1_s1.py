# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def run_bell_state_simulator():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.Measure(q[0], c[0]))
    prog.insert(pq.Measure(q[1], c[1]))

    shots = 1000
    counts = pq.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    pq.destroy_quantum_machine(machine)
    return probs
