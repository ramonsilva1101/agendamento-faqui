import sqlite3

def criar_banco():
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recurso TEXT NOT NULL,
            data_reserva TEXT NOT NULL,
            horario TEXT NOT NULL,
            email_usuario TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def salvar_reserva(recurso, data, horario, email):
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO agendamentos (recurso, data_reserva, horario, email_usuario)
        VALUES (?, ?, ?, ?)
    ''', (recurso, str(data), horario, email))
    conn.commit()
    conn.close()

def listar_reservas():
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, recurso, data_reserva, horario, email_usuario FROM agendamentos')
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- NOVA FUNÇÃO PARA O CALENDÁRIO VISUAL ---
def listar_reservas_por_recurso(recurso):
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    # Busca apenas datas e horários de um recurso específico
    cursor.execute('SELECT data_reserva, horario FROM agendamentos WHERE recurso = ?', (recurso,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def verificar_disponibilidade(recurso, data, horario):
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM agendamentos 
        WHERE recurso = ? AND data_reserva = ? AND horario = ?
    ''', (recurso, str(data), horario))
    resultado = cursor.fetchone() 
    conn.close()
    
    if resultado is not None:
        return False
    else:
        return True

def deletar_reserva(id_reserva):
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM agendamentos WHERE id = ?', (id_reserva,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_banco()