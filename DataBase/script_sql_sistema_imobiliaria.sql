CREATE TABLE "imovel"(
    "id" INTEGER NOT NULL,
    "logradouro" CHAR(255) NOT NULL,
    "cep" VARCHAR(255) NOT NULL,
    "bairro" CHAR(255) NOT NULL,
    "cidade" CHAR(255) NOT NULL,
    "id_proprietario" INTEGER NOT NULL,
    "valor" INTEGER NOT NULL
);
ALTER TABLE
    "imovel" ADD PRIMARY KEY("id");
CREATE TABLE "aluguel"(
    "id" INTEGER NOT NULL,
    "id_imovel" INTEGER NOT NULL,
    "id_inquilino" INTEGER NOT NULL,
    "id_corretor" INTEGER NOT NULL
);
ALTER TABLE
    "aluguel" ADD PRIMARY KEY("id");
CREATE TABLE "inquilino"(
    "id" INTEGER NOT NULL,
    "nome" CHAR(255) NOT NULL,
    "data_nascimento" DATE NOT NULL,
    "telefone" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "inquilino" ADD PRIMARY KEY("id");
CREATE TABLE "proprietario"(
    "id" INTEGER NOT NULL,
    "nome" CHAR(255) NOT NULL,
    "data_nascimento" DATE NOT NULL,
    "telefone" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "proprietario" ADD PRIMARY KEY("id");
CREATE TABLE "corretor"(
    "id" INTEGER NOT NULL,
    "nome" CHAR(255) NOT NULL,
    "data_entrada" DATE NOT NULL,
    "data_nascimento" DATE NOT NULL
);
ALTER TABLE
    "corretor" ADD PRIMARY KEY("id");
ALTER TABLE
    "aluguel" ADD CONSTRAINT "aluguel_id_imovel_foreign" FOREIGN KEY("id_imovel") REFERENCES "imovel"("id");
ALTER TABLE
    "aluguel" ADD CONSTRAINT "aluguel_id_inquilino_foreign" FOREIGN KEY("id_inquilino") REFERENCES "inquilino"("id");
ALTER TABLE
    "imovel" ADD CONSTRAINT "imovel_id_proprietario_foreign" FOREIGN KEY("id_proprietario") REFERENCES "proprietario"("id");
ALTER TABLE
    "aluguel" ADD CONSTRAINT "aluguel_id_corretor_foreign" FOREIGN KEY("id_corretor") REFERENCES "corretor"("id");