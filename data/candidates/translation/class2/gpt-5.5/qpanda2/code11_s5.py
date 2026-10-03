# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    prog = pq.QProg()
    try:
        prog << circuit
    except Exception:
        try:
            prog.insert(circuit)
        except Exception:
            prog = circuit

    def _addr(obj):
        for name in ("get_phy_addr", "get_addr"):
            try:
                return int(getattr(obj, name)())
            except Exception:
                pass
        try:
            return int(obj)
        except Exception:
            return None

    max_qaddr = -1
    try:
        used_qubits = pq.get_all_used_qubits(prog)
        for qubit in used_qubits:
            addr = _addr(qubit)
            if addr is not None and addr > max_qaddr:
                max_qaddr = addr
    except Exception:
        try:
            n_qubits = int(pq.get_qprog_qubit_num(prog))
            max_qaddr = max(max_qaddr, n_qubits - 1)
        except Exception:
            pass

    max_caddr = -1
    try:
        used_cbits = pq.get_all_used_class_bits(prog)
        for cbit in used_cbits:
            addr = _addr(cbit)
            if addr is not None and addr > max_caddr:
                max_caddr = addr
    except Exception:
        try:
            n_cbits = int(pq.get_qprog_cbit_num(prog))
            max_caddr = max(max_caddr, n_cbits - 1)
        except Exception:
            pass

    qvm = pq.CPUQVM()
    try:
        try:
            qvm.set_configure(max(max_qaddr + 1, 1), max(max_caddr + 1, 1))
        except Exception:
            pass
        qvm.init_qvm()
        if max_qaddr >= 0:
            qvm.qAlloc_many(max_qaddr + 1)
        if max_caddr >= 0:
            qvm.cAlloc_many(max_caddr + 1)
        qvm.directly_run(prog)
        state = list(qvm.get_qstate())
        qvm.finalize()
        return state
    except Exception as exc:
        try:
            qvm.finalize()
        except Exception:
            pass
        try:
            pq.directly_run(prog)
            return list(pq.get_qstate())
        except Exception:
            raise exc
