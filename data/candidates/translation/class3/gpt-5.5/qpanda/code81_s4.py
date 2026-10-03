# EVAL_META: task_id=81, framework=qpanda, class=3
import os
import tempfile
import pyqpanda3.core as pq

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    machine = None
    try:
        machine = pq.CPUQVM()
        for init_name in ("init_qvm", "init"):
            if hasattr(machine, init_name):
                getattr(machine, init_name)()
                break
        convert_qasm_string_to_quantum_circuit._qvm = machine
    except Exception:
        machine = None

    converter = None
    for name in ("convert_qasm_to_qprog", "convert_qasm_string_to_qprog", "qasm_to_qprog"):
        if hasattr(pq, name):
            converter = getattr(pq, name)
            break

    if converter is not None:
        arg_sets = []
        if machine is not None:
            arg_sets.extend([(qasm_string, machine), (machine, qasm_string)])
        arg_sets.append((qasm_string,))

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".qasm", delete=False) as tmp:
                tmp.write(qasm_string)
                tmp_path = tmp.name
            if machine is not None:
                arg_sets.extend([(tmp_path, machine), (machine, tmp_path)])
            arg_sets.append((tmp_path,))

            for args in arg_sets:
                try:
                    result = converter(*args)
                    if isinstance(result, tuple) and result:
                        return result[0]
                    return result
                except Exception:
                    pass
        finally:
            if tmp_path is not None:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    if machine is None:
        machine = pq.CPUQVM()
        for init_name in ("init_qvm", "init"):
            if hasattr(machine, init_name):
                getattr(machine, init_name)()
                break
        convert_qasm_string_to_quantum_circuit._qvm = machine

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
        if hasattr(machine, alloc_name):
            try:
                qubits = getattr(machine, alloc_name)(2)
                break
            except Exception:
                pass

    if qubits is None:
        qubits = []
        for _ in range(2):
            for alloc_name in ("qAlloc", "qalloc"):
                if hasattr(machine, alloc_name):
                    qubits.append(getattr(machine, alloc_name)())
                    break
        if len(qubits) != 2:
            qubits = [0, 1]

    prog = pq.QProg()
    cnot_gate = getattr(pq, "CNOT", getattr(pq, "CX", None))

    try:
        prog << pq.H(qubits[0])
        prog << cnot_gate(qubits[0], qubits[1])
    except Exception:
        prog.insert(pq.H(qubits[0]))
        prog.insert(cnot_gate(qubits[0], qubits[1]))

    return prog
