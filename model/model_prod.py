import mysql.connector
from database.database import get_cursor
from dotenv import load_dotenv
import os

load_dotenv()

def criar_banco_dados(database=None):
    with get_cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DB')}")
        print(f"Database {os.getenv('MYSQL_DB')} created or already exists")

def criar_tabela_produtos():
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        print("Creating table usuario...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produto (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    descricao TEXT,
                    preco DECIMAL(10, 2) NOT NULL,
                    estoque INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def criar_produto(nome, descricao, preco, estoque):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("""
                INSERT INTO produto (nome, descricao, preco, estoque)
                VALUES (%s, %s, %s, %s)
            """, (nome, descricao, preco, estoque))
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def listar_produtos():
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("SELECT * FROM produto")
            produtos = cursor.fetchall()
            print(f"Produtos encontrados: {produtos}")
            return produtos
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")
            return []

def obter_produto_por_id(produto_id):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("SELECT * FROM produto WHERE id = %s", (produto_id,))
            produto = cursor.fetchone()
            return produto
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def atualizar_produto(produto_id, nome=None, descricao=None, preco=None, estoque=None):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("""
                UPDATE produto
                SET nome = COALESCE(%s, nome),
                    descricao = COALESCE(%s, descricao),
                    preco = COALESCE(%s, preco),
                    estoque = COALESCE(%s, estoque)
                WHERE id = %s
            """, (nome, descricao, preco, estoque, produto_id))
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")

def deletar_produto(produto_id):
    with get_cursor(database = os.getenv('MYSQL_DB')) as cursor:
        try:
            cursor.execute("DELETE FROM produto WHERE id = %s", (produto_id,))
        except mysql.connector.Error as e:
            print(f"Error MySQL: {e}")