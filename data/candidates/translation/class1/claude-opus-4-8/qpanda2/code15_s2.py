# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def noisy_bell():
    shots = 1000
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.set_noise_model(pq.NoiseModel.DEPOLARIZING_KRAUS_ERROR, pq.GateType.HADAMARD_GATE, 0.01)
    machine.set_noise_model(pq.NoiseModel.DEPOLARIZING_KRAUS_ERROR, pq.GateType.CNOT_GATE, 0.02)

    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.measure_all(qubits, cbits)

    counts = machine.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(counts.values())
    result = {key: value / total for key, value in counts.items()}

    machine.finalize()
    return result
