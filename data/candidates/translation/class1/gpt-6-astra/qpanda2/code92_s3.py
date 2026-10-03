# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        program = QProg()
        program << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        machine.directly_run(program)
        state = machine.get_qstate()
        return {
            format(index, "02b"): float(abs(amplitude) ** 2)
            for index, amplitude in enumerate(state)
            if abs(amplitude) ** 2 > 1e-15
        }
    finally:
        machine.finalize()
