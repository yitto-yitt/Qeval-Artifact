# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import *

def get_statevector(circuit):
    try:
        prog = QProg()
        prog << circuit
    except Exception:
        prog = circuit

    try:
        directly_run(prog)
        return get_qstate()
    except Exception:
        qvm = CPUQVM()
        qvm.init_qvm()
        try:
            qubit_count = 0
            try:
                used_qubits = get_all_used_qubits(prog)
                max_addr = -1
                for q in used_qubits:
                    try:
                        addr = q.get_phy_addr()
                    except Exception:
                        addr = q.getPhysicalQubitPtr().getQubitAddr()
                    if addr > max_addr:
                        max_addr = addr
                qubit_count = max_addr + 1
            except Exception:
                qubit_count = 0

            if qubit_count > 0:
                qvm.qAlloc_many(qubit_count)

            qvm.directly_run(prog)
            state = qvm.get_qstate()
            return state
        finally:
            qvm.finalize()
