# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
import re
import atexit

machine = CPUQVM()
try:
    machine.set_configure(64, 64)
except Exception:
    pass
machine.init_qvm()
q = machine.qAlloc_many(64)
c = machine.cAlloc_many(64)

_NUMERIC_ALLOWED_RE = re.compile(r"^[0-9eE\.\+\-\*/\(\),\s]*$")
_IDENTIFIER_RE = re.compile(r"[A-Za-z_]\w*")
_PARAM_GATE_NAMES = {
    "RX", "RY", "RZ", "U1", "U2", "U3", "U4", "CU", "CR", "CP", "CU1", "CU2", "CU3",
    "RXX", "RYY", "RZZ", "RZX", "ISWAP", "PHASE", "P"
}
_ALLOWED_CONSTANTS = {"pi", "PI", "Pi", "e", "E"}


def _param_is_unassigned(param):
    if hasattr(param, "parameters"):
        try:
            return len(param.parameters) > 0
        except Exception:
            pass
    if hasattr(param, "free_symbols"):
        try:
            return len(param.free_symbols) > 0
        except Exception:
            pass
    try:
        float(param)
        return False
    except Exception:
        pass
    text = str(param)
    if text in _ALLOWED_CONSTANTS:
        return False
    identifiers = _IDENTIFIER_RE.findall(text)
    return any(identifier not in _ALLOWED_CONSTANTS for identifier in identifiers)


def _line_has_unassigned_parameter(line):
    stripped = line.strip()
    if not stripped or stripped.startswith("//"):
        return False
    op = stripped.split(None, 1)[0].upper()
    if op not in _PARAM_GATE_NAMES:
        return False
    if "," not in stripped:
        return False
    text = re.sub(r"[qc]\[\d+\]", "", stripped, flags=re.IGNORECASE)
    text = text[len(stripped.split(None, 1)[0]):]
    identifiers = _IDENTIFIER_RE.findall(text)
    identifiers = [identifier for identifier in identifiers if identifier not in _ALLOWED_CONSTANTS]
    return len(identifiers) > 0


def _filter_originir(originir):
    filtered_lines = []
    for line in originir.splitlines():
        if not _line_has_unassigned_parameter(line):
            filtered_lines.append(line)
    if filtered_lines and filtered_lines[-1].strip().upper() != "END":
        filtered_lines.append("END")
    return "\n".join(filtered_lines)


def remove_unassigned_parameterized_gates(circuit):
    if hasattr(circuit, "data"):
        try:
            new_circuit = circuit.copy_empty_like()
        except Exception:
            new_circuit = circuit.__class__(circuit.num_qubits, circuit.num_clbits)

        for instruction in list(circuit.data):
            instr = getattr(instruction, "operation", instruction[0])
            qargs = getattr(instruction, "qubits", instruction[1])
            cargs = getattr(instruction, "clbits", instruction[2])
            params = getattr(instr, "params", [])

            if not any(_param_is_unassigned(param) for param in params):
                try:
                    q_indices = [circuit.find_bit(bit).index for bit in qargs]
                    c_indices = [circuit.find_bit(bit).index for bit in cargs]
                    new_circuit.append(instr, q_indices, c_indices)
                except Exception:
                    new_circuit.append(instr, qargs, cargs)
        return new_circuit

    prog = QProg()
    try:
        prog.insert(circuit)
    except Exception:
        prog = circuit

    originir = convert_qprog_to_originir(prog, machine)
    filtered_originir = _filter_originir(originir)
    return convert_originir_to_qprog(filtered_originir, machine)


atexit.register(machine.finalize)
