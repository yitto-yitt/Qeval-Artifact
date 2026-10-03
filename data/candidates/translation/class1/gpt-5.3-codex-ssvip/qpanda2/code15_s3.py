# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def noisy_bell():
    shots = 1000
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.measure_all(q, c)

    noise = pq.NoiseQVM()
    noise.init_qvm()

    noise_model = pq.NoiseModel()
    noise_model.add_noise_model(pq.NOISE_MODEL.DEPOLARIZING_KRAUS_OPERATOR, pq.GateType.HADAMARD_GATE, 0.001)
    noise_model.add_noise_model(pq.NOISE_MODEL.DEPOLARIZING_KRAUS_OPERATOR, pq.GateType.CNOT_GATE, 0.01)
    noise.set_noise_model(noise_model)

    qn = noise.qAlloc_many(2)
    cn = noise.cAlloc_many(2)
    noisy_prog = pq.QProg()
    noisy_prog << pq.H(qn[0]) << pq.CNOT(qn[0], qn[1]) << pq.measure_all(qn, cn)

    counts = noise.run_with_configuration(noisy_prog, cn, shots)
    total = builtins.sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    machine.finalize()
    noise.finalize()
    return probs
