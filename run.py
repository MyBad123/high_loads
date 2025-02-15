import os
import subprocess
import argparse

def setup_replication(primary_host, primary_port, primary_user, primary_password, replica_host, replica_port, replica_user, replica_password, replication_slot, replication_user):
    """
    Настраивает репликацию базы данных PostgreSQL.

    :param primary_host: Хост основного сервера
    :param primary_port: Порт основного сервера
    :param primary_user: Пользователь основного сервера
    :param primary_password: Пароль пользователя основного сервера
    :param replica_host: Хост реплики
    :param replica_port: Порт реплики
    :param replica_user: Пользователь реплики
    :param replica_password: Пароль пользователя реплики
    :param replication_slot: Имя слота репликации
    :param replication_user: Пользователь для репликации
    """
    try:
        # Устанавливаем переменные окружения для паролей
        os.environ['PGPASSWORD'] = primary_password

        # Создаем слот репликации на основном сервере
        create_slot_command = [
            "psql",
            "-h", primary_host,
            "-p", str(primary_port),
            "-U", primary_user,
            "-c", f"SELECT * FROM pg_create_physical_replication_slot('{replication_slot}');"
        ]
        subprocess.run(create_slot_command, check=True)
        print(f"Слот репликации '{replication_slot}' успешно создан на основном сервере.")

        # Настраиваем реплику
        os.environ['PGPASSWORD'] = replica_password

        # Останавливаем реплику (если она запущена)
        subprocess.run(["pg_ctl", "stop", "-D", "/var/lib/postgresql/data"], check=True)

        # Копируем данные с основного сервера на реплику
        basebackup_command = [
            "pg_basebackup",
            "-h", primary_host,
            "-p", str(primary_port),
            "-U", replication_user,
            "-D", "/var/lib/postgresql/data",
            "-Fp",
            "-Xs",
            "-P",
            "-R"
        ]
        subprocess.run(basebackup_command, check=True)
        print("База данных успешно скопирована на реплику.")

        # Запускаем реплику
        subprocess.run(["pg_ctl", "start", "-D", "/var/lib/postgresql/data"], check=True)
        print("Реплика успешно запущена.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при настройке репликации: {e}")
    finally:
        # Удаляем переменные окружения для безопасности
        os.environ.pop('PGPASSWORD', None)

if __name__ == "__main__":
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Настройка репликации базы данных PostgreSQL.")
    parser.add_argument("--primary_host", required=True, help="Хост основного сервера")
    parser.add_argument("--primary_port", type=int, default=5432, help="Порт основного сервера (по умолчанию 5432)")
    parser.add_argument("--primary_user", required=True, help="Пользователь основного сервера")
    parser.add_argument("--primary_password", required=True, help="Пароль пользователя основного сервера")
    parser.add_argument("--replica_host", required=True, help="Хост реплики")
    parser.add_argument("--replica_port", type=int, default=5432, help="Порт реплики (по умолчанию 5432)")
    parser.add_argument("--replica_user", required=True, help="Пользователь реплики")
    parser.add_argument("--replica_password", required=True, help="Пароль пользователя реплики")
    parser.add_argument("--replication_slot", required=True, help="Имя слота репликации")
    parser.add_argument("--replication_user", required=True, help="Пользователь для репликации")

    args = parser.parse_args()

    # Вызываем функцию настройки репликации
    setup_replication(
        primary_host=args.primary_host,
        primary_port=args.primary_port,
        primary_user=args.primary_user,
        primary_password=args.primary_password,
        replica_host=args.replica_host,
        replica_port=args.replica_port,
        replica_user=args.replica_user,
        replica_password=args.replica_password,
        replication_slot=args.replication_slot,
        replication_user=args.replication_user
    )
