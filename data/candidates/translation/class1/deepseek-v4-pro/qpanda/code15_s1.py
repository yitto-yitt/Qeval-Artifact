# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import (
    QVM,
    QProg,
    QCircuit,
    NoiseModel,
    c_optimize_qcircuit,
    H,
    CNOT,
    Measure,
)

def noisy_bell():
    # Build Bell circuit (2 qubits)
    prog = QProg()
    prog << H(0) << CNOT(0, 1)
    # add measurements (all qubits)
    # QPanda uses classical bits; we need two classical bits
    # create classical register implicit with Measure
    prog << Measure(0, 0) << Measure(1, 1)

    # Convert to QCircuit for optimization
    circ = QCircuit(prog)

    # Optimization level 1 (similar to Qiskit's preset pass manager)
    optimized_circ = c_optimize_qcircuit(circ, 1)

    # Build a noise model mimicking a typical superconducting device
    noise_model = NoiseModel()
    # Single-qubit depolarizing error (1e-3)
    noise_model.add_noise_model(NoiseModel.SINGLE_GATE_TYPE, 
                                NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, 0.001)
    # Two-qubit depolarizing (1e-2)
    noise_model.add_noise_model(NoiseModel.DOUBLE_GATE_TYPE, 
                                NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, 0.01)
    # Readout errors: bit flip on measurement (probability of bit flip 0.05)
    noise_model.add_noise_model(NoiseModel.READOUT_GATE_TYPE, 
                                NoiseModel.BITFLIP_KRAUS_OPERATOR, 0.05)

    # Initialize quantum virtual machine with noise model
    qvm = QVM()
    qvm.set_noise_model(noise_model)

    # Run with 1000 shots
    result = qvm.directly_run_with_noise(optimized_circ, 1000)
    counts = result.get_counts()

    # Normalize to probabilities
    total = sum(counts.values())
    if total == 0:
        return {"00": 0.0}  # safeguard
    return {k: v / total for k, v in counts.items()}
