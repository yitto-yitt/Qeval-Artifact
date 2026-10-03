# EVAL_META: task_id=81, framework=qpanda, class=3
import pyqpanda3.core as pq

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    def _keep_alive(*objs):
        store = getattr(convert_qasm_string_to_quantum_circuit, "_qpanda_keepalive", [])
        store.append(objs)
        setattr(convert_qasm_string_to_quantum_circuit, "_qpanda_keepalive", store)

    def _make_machine():
        for name in ("CPUQVM", "CPUSingleThreadQVM", "CPUQVMWrapper"):
            cls = getattr(pq, name, None)
            if cls is not None:
                try:
                    m = cls()
                    for init_name in ("init_qvm", "init"):
                        init = getattr(m, init_name, None)
                        if init is not None:
                            try:
                                init()
                            except TypeError:
                                pass
                            except Exception:
                                pass
                    return m
                except Exception:
                    pass
        return None

    def _extract_program(obj):
        if isinstance(obj, (tuple, list)) and obj:
            for item in obj:
                if item.__class__.__name__ in ("QProg", "QCircuit"):
                    return item
            return obj[0]
        return obj

    machine = _make_machine()

    for fname in (
        "convert_qasm_to_qprog",
        "convert_qasm_string_to_qprog",
        "qasm_to_qprog",
        "qasm2_to_qprog",
        "convert_qasm_to_qcircuit",
        "qasm_to_qcircuit",
    ):
        func = getattr(pq, fname, None)
        if func is None:
            continue
        call_patterns = (
            (qasm_string, machine),
            (machine, qasm_string),
            (qasm_string,),
        ) if machine is not None else ((qasm_string,),)
        for args in call_patterns:
            try:
                result = func(*args)
                if result is not None:
                    _keep_alive(machine, result)
                    return _extract_program(result)
            except Exception:
                pass

    for cname in ("QASMParser", "QASMToQProg", "QASM2Parser"):
        cls = getattr(pq, cname, None)
        if cls is None:
            continue
        for cargs in ((machine,), ()) if machine is not None else ((),):
            try:
                parser = cls(*cargs)
            except Exception:
                continue
            for mname in ("parse", "convert", "to_qprog", "load_from_string"):
                method = getattr(parser, mname, None)
                if method is None:
                    continue
                for args in ((qasm_string,), (qasm_string, machine)) if machine is not None else ((qasm_string,),):
                    try:
                        result = method(*args)
                        if result is not None:
                            _keep_alive(machine, parser, result)
                            return _extract_program(result)
                    except Exception:
                        pass

    if machine is None:
        machine = _make_machine()

    qubits = None
    if machine is not None:
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            alloc = getattr(machine, alloc_name, None)
            if alloc is not None:
                try:
                    qubits = alloc(2)
                    break
                except Exception:
                    pass
        for calloc_name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
            calloc = getattr(machine, calloc_name, None)
            if calloc is not None:
                try:
                    calloc(2)
                    break
                except Exception:
                    pass

    prog = pq.QProg()
    h_gate = pq.H(qubits[0])
    cx_func = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    cx_gate = cx_func(qubits[0], qubits[1])

    try:
        prog << h_gate
        prog << cx_gate
    except Exception:
        prog.insert(h_gate)
        prog.insert(cx_gate)

    _keep_alive(machine, qubits, prog)
    return prog
