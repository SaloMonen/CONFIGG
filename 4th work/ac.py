import sys
import yaml

# Определяем команды
COMMANDS = {
    'LOAD_CONST': 30,
    'READ_MEM': 8,
    'WRITE_MEM': 11,
    'POPCNT': 39
}


# Функция для преобразования строковой команды в байтовое представление
def assemble_command(line):
    parts = line.split()
    cmd = parts[0]

    if cmd not in COMMANDS:
        raise ValueError(f"Неизвестная команда: {cmd}")

    A = COMMANDS[cmd]
    B = int(parts[1])
    C = int(parts[2])

    # сборка байтовой команды
    byte_command = bytearray(5)
    byte_command[0] = A
    byte_command[1] = (B >> 8) & 0xFF
    byte_command[2] = B & 0xFF
    byte_command[3] = (C >> 8) & 0xFF
    byte_command[4] = C & 0xFF

    return byte_command


def assemble(input_file, output_file, log_file):
    commands = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                cmd_bytes = assemble_command(line.strip())
                commands.append({'cmd': line.strip(), 'bytes': list(cmd_bytes)})

    # Записываем в бинарный файл
    with open(output_file, 'wb') as f:
        f.write(b''.join(commands))

    # Лог в формате YAML
    with open(log_file, 'w') as f:
        yaml.dump(commands, f)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assemble(input_file, output_file, log_file)