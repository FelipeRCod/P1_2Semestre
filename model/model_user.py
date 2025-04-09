import mysql.connector
from database.database import get_cursor
from dotenv import load_dotenv
import os

load_dotenv()
def criar_banco_dados():
    with get_cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DB')}")
        print(f"Database {os.getenv('MYSQL_DB')} created or already exists")

def criar_tabela_usuarios():
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        print("Creating table usuario...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    senha VARCHAR(255) NOT NULL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def criar_usuario(nome, email, senha):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("""
                INSERT INTO usuario (nome, email, senha)
                VALUES (%s, %s, %s)
            """, (nome, email, senha))
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def listar_usuarios():
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("SELECT * FROM usuario")
            usuarios = cursor.fetchall()
            return usuarios
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def buscar_usuario_por_id(usuario_id):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
            usuario = cursor.fetchone()
            return usuario
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def atualizar_usuario(usuario_id, nome=None, email=None, senha=None):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("""
                UPDATE usuario
                    SET nome = COALESCE(%s, nome),
                    email = COALESCE(%s, email),
                    senha = COALESCE(%s, senha)
                WHERE id = %s
            """ , (nome, email, senha, usuario_id))
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def deletar_usuario(id):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")