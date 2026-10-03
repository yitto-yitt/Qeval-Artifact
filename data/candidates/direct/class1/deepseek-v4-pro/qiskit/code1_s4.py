# EVAL_META: task_id=1, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def run_bell_state_simulator():
    # Create the |Phi+> Bell state
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator()

    # Transpile with a preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)

    shots = 1024
    sampler = SamplerV2(backend=backend)
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result()

    data = result[0].data

    counts = None
    if hasattr(data, "meas"):
        counts = data.meas.get_counts()

    if counts is None:
        for field_name in dir(data):
            if field_name.startswith("_"):
                continue
            field = getattr(data, field_name)
            if hasattr(field, "get_counts"):
                counts = field.get_counts()
                break

    if counts is None:
        raise RuntimeError("Could not extract measurement counts from SamplerV2 result.")

    return {bitstring: count / shots for bitstring, count in counts.items()}
