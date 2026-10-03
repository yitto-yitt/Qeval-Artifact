# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def bell_each_shot():
    shots = 10
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.Measure(q[0], c[0]))
    prog.insert(pq.Measure(q[1], c[1]))

    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    result = {k: v / total for k, v in counts.items()}

    pq.destroy_quantum_machine(machine)
    return result
