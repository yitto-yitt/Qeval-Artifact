# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def noisy_bell():
    shots = 1000
    machine = pq.init_quantum_machine(pq.QMachineType.NOISE)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    noise = pq.Noise()
    noise.add_noise_model(pq.NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, pq.GateType.HADAMARD_GATE, 0.001)
    noise.add_noise_model(pq.NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, pq.GateType.CNOT_GATE, 0.01)
    machine.set_noise_model(noise)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.measure_all(q, c))

    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    pq.destroy_quantum_machine(machine)
    return probs
