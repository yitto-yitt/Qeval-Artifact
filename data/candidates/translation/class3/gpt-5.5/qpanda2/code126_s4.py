# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def calculate_phase_difference_fidelity():
    try:
        try:
            gate = pq.H(qubits[0])
            try:
                raw_matrix = gate.get_matrix()
            except Exception:
                raw_matrix = pq.get_matrix(gate)
            op_a = np.array(raw_matrix, dtype=complex).reshape((2, 2))
        except Exception:
            columns = []
            for prepare_one in (False, True):
                try:
                    machine.init_state()
                except Exception:
                    pass
                prog = pq.QProg()
                try:
                    prog << pq.Reset(qubits[0])
                except Exception:
                    pass
                if prepare_one:
                    prog << pq.X(qubits[0])
                prog << pq.H(qubits[0])
                machine.directly_run(prog)
                columns.append(np.array(machine.get_qstate(), dtype=complex)[:2])
            op_a = np.column_stack(columns)

        op_b = np.exp(1j * 0.5) * op_a
        dim = op_a.shape[0]
        fidelity = (abs(np.trace(np.conjugate(op_a.T) @ op_b)) ** 2) / (dim ** 2)
        return float(round(float(np.real_if_close(fidelity)), 15))
    finally:
        machine.finalize()
