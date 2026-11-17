-- Projeto físico do banco de dados - Controle de Estoque (MySQL 8)
CREATE DATABASE IF NOT EXISTS estoque CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE estoque;

CREATE TABLE categoria (
    id   INT          NOT NULL AUTO_INCREMENT,
    nome VARCHAR(60)  NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uq_categoria_nome UNIQUE (nome)
) ENGINE=InnoDB;

CREATE TABLE produto (
    id             INT            NOT NULL AUTO_INCREMENT,
    nome           VARCHAR(100)   NOT NULL,
    sku            VARCHAR(30)    NOT NULL,
    preco          DECIMAL(10,2)  NOT NULL,
    quantidade     INT            NOT NULL DEFAULT 0,
    estoque_minimo INT            NOT NULL DEFAULT 0,
    categoria_id   INT            NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uq_produto_sku UNIQUE (sku),
    CONSTRAINT fk_produto_categoria FOREIGN KEY (categoria_id) REFERENCES categoria (id),
    CONSTRAINT ck_produto_preco CHECK (preco >= 0),
    CONSTRAINT ck_produto_qtd CHECK (quantidade >= 0),
    CONSTRAINT ck_produto_min CHECK (estoque_minimo >= 0)
) ENGINE=InnoDB;

CREATE TABLE movimentacao (
    id         INT          NOT NULL AUTO_INCREMENT,
    produto_id INT          NOT NULL,
    tipo       VARCHAR(7)   NOT NULL,
    quantidade INT          NOT NULL,
    data_hora  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacao VARCHAR(200) NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_mov_produto FOREIGN KEY (produto_id) REFERENCES produto (id) ON DELETE CASCADE,
    CONSTRAINT ck_mov_tipo CHECK (tipo IN ('ENTRADA','SAIDA')),
    CONSTRAINT ck_mov_qtd CHECK (quantidade > 0)
) ENGINE=InnoDB;

CREATE INDEX idx_produto_nome ON produto (nome);
CREATE INDEX idx_mov_produto_data ON movimentacao (produto_id, data_hora);

-- Dados de exemplo (opcional)
INSERT INTO categoria (nome) VALUES ('Bebidas'), ('Limpeza'), ('Mercearia');
INSERT INTO produto (nome, sku, preco, quantidade, estoque_minimo, categoria_id) VALUES
 ('Suco de Laranja 1L', 'SUC-001', 7.50, 20, 5, 1),
 ('Detergente 500ml',   'DET-001', 2.99, 3, 5, 2),
 ('Arroz 5kg',          'ARR-001', 28.90, 12, 4, 3);
