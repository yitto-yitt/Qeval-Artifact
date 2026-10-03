# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        program = pq.QProg()
        program << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
        probabilities = machine.prob_run_dict(program, qubits, -1)
        return {
            outcome: float(probability)
            for outcome, probability in probabilities.items()
            if probability > 0.0
        }
    finally:
        machine.finalize()
