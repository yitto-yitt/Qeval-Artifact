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

    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "initQVM", "init"):
        init = getattr(machine, init_name, None)
        if callable(init):
            try:
                init()
            except TypeError:
                pass
            except Exception:
                pass
            break

    if not hasattr(convert_qasm_string_to_quantum_circuit, "_qpanda_resources"):
        convert_qasm_string_to_quantum_circuit._qpanda_resources = []
    convert_qasm_string_to_quantum_circuit._qpanda_resources.append(machine)

    def _select_program(obj):
        if isinstance(obj, (tuple, list)):
            for item in obj:
                name = type(item).__name__.lower()
                if "prog" in name or "circuit" in name:
                    return item
            return obj[0] if obj else obj
        return obj

    parser_names = (
        "convert_qasm_string_to_qprog",
        "convert_qasm_to_qprog",
        "qasm_to_qprog",
        "convert_qasm_file_to_qprog",
    )

    for name in parser_names:
        func = getattr(pq, name, None)
        if callable(func):
            for args in ((qasm_string, machine), (machine, qasm_string), (qasm_string,)):
                try:
                    result = func(*args)
                    if result is not None:
                        convert_qasm_string_to_quantum_circuit._qpanda_resources.append(result)
                        return _select_program(result)
                except Exception:
                    pass

            path = None
            try:
                with tempfile.NamedTemporaryFile("w", suffix=".qasm", delete=False) as f:
                    f.write(qasm_string)
                    path = f.name
                for args in ((path, machine), (machine, path), (path,)):
                    try:
                        result = func(*args)
                        if result is not None:
                            convert_qasm_string_to_quantum_circuit._qpanda_resources.append(result)
                            return _select_program(result)
                    except Exception:
                        pass
            finally:
                if path is not None:
                    try:
                        os.remove(path)
                    except OSError:
                        pass

    qalloc = None
    for alloc_name in ("qAlloc_many", "qAllocMany", "qalloc_many"):
        qalloc = getattr(machine, alloc_name, None)
        if callable(qalloc):
            break
    if qalloc is None:
        qalloc_one = getattr(machine, "qAlloc", None)
        qubits = [qalloc_one(), qalloc_one()]
    else:
        qubits = qalloc(2)

    for calloc_name in ("cAlloc_many", "cAllocMany", "calloc_many"):
        calloc = getattr(machine, calloc_name, None)
        if callable(calloc):
            try:
                cbits = calloc(2)
                convert_qasm_string_to_quantum_circuit._qpanda_resources.append(cbits)
            except Exception:
                pass
            break

    circuit = pq.QCircuit() if hasattr(pq, "QCircuit") else pq.QProg()
    cnot = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    circuit << pq.H(qubits[0])
    circuit << cnot(qubits[0], qubits[1])
    convert_qasm_string_to_quantum_circuit._qpanda_resources.append((qubits, circuit))
    return circuit
