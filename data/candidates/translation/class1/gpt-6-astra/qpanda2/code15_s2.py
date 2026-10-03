# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def noisy_bell():
    machine = pq.NoiseQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        cbits = machine.cAlloc_many(2)

        machine.set_noise_model(
            pq.NoiseModel.DEPOLARIZING_KRAUS_OPERATOR,
            pq.GateType.HADAMARD_GATE,
            0.001,
        )
        machine.set_noise_model(
            pq.NoiseModel.DEPOLARIZING_KRAUS_OPERATOR,
            pq.GateType.CNOT_GATE,
            0.02,
        )
        machine.set_readout_error(
            [[0.98, 0.02], [0.02, 0.98]], qubits
        )

        program = pq.QProg()
        program << pq.H(qubits[0])
        program << pq.CNOT(qubits[0], qubits[1])
        program << pq.Measure(qubits[0], cbits[0])
        program << pq.Measure(qubits[1], cbits[1])

        counts = machine.run_with_configuration(program, cbits, 1000)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        machine.finalize()
