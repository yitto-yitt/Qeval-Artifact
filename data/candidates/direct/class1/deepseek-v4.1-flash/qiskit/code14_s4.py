# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_qc = pm.run(qc)

    try:
        from qiskit_ibm_runtime import SamplerV2 as Sampler
        sampler = Sampler(mode=backend)
        sampler.options.default_shots = 10
        job = sampler.run([isa_qc])
        result = job.result()
        pub_result = result[0]
        counts = pub_result.data.meas.get_counts()
    except Exception:
        from qiskit_ibm_runtime import Sampler
        sampler = Sampler(backend=backend)
        sampler.options.shots = 10
        job = sampler.run(isa_qc)
        result = job.result()
        quasi_dists = result.quasi_dists[0]
        counts = {format(k, '02b'): round(v * 10) for k, v in quasi_dists.items()}

    return {bitstring: count / 10 for bitstring, count in counts.items()}
