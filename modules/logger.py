import sqlite3

def save_event(
    timestamp,
    event_type,
    file_name,
    source_path,
    destination_path,
    username,
    process_name,
    hash_before,
    hash_after,
    integrity_status,
    sensitive,
    authorized,
    status
):

    conn = sqlite3.connect("database/filemonitor.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO file_events
        (
            timestamp,
            event_type,
            file_name,
            source_path,
            destination_path,
            username,
            process_name,
            hash_before,
            hash_after,
            integrity_status,
            sensitive,
            authorized,
            status
        )

        VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,

        (
            timestamp,
            event_type,
            file_name,
            source_path,
            destination_path,
            username,
            process_name,
            hash_before,
            hash_after,
            integrity_status,
            sensitive,
            authorized,
            status
        )

    )

    conn.commit()
    conn.close()
