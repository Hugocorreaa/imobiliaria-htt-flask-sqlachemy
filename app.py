from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2315@localhost:5432/imobiliaria-htt'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# ===== Criação das Tabelas ======

class Inquilino(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    data_nascimento = db.Column(db.Date())
    telefone = db.Column(db.String())

    def __init__(self, nome, data_nascimento, telefone):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone

class Proprietario(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    data_nascimento = db.Column(db.Date())
    telefone = db.Column(db.String())

    def __init__(self, nome, data_nascimento, telefone):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone

class Corretor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    data_nascimento = db.Column(db.Date())
    telefone = db.Column(db.String())

    def __init__(self, nome, data_nascimento, telefone):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone

class Imovel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String())
    cep = db.Column(db.String())
    bairro = db.Column(db.String())
    cidade = db.Column(db.String())
    id_proprietario = db.Column(db.Integer(), db.ForeignKey(
        'proprietario.id'), nullable=False)
    valor = db.Column(db.Float())

    def __init__(self, logradouro, cep, bairro, cidade, id_proprietario, valor):
        self.logradouro = logradouro
        self.cep = cep
        self.bairro = bairro
        self.cidade = cidade
        self.id_proprietario = id_proprietario
        self.valor = valor

class Aluguel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_imovel = db.Column(db.Integer(), db.ForeignKey(
        'imovel.id'), nullable=False)
    id_inquilino = db.Column(db.Integer(), db.ForeignKey(
        'inquilino.id'), nullable=False)
    id_corretor = db.Column(db.Integer(), db.ForeignKey(
        'corretor.id'), nullable=False)

    def __init__(self, id_imovel, id_inquilino, id_corretor):
        self.id_imovel = id_imovel
        self.id_inquilino = id_inquilino
        self.id_corretor = id_corretor


# ======= Rotas ========
@app.route('/')
def index():
    return render_template('menu.html')

# Inquilinos
@app.route('/show_all_inquilinos')
def show_all_inquilinos():
    return render_template('inquilino/show_all_inquilinos.html', inquilinos=Inquilino.query.all())

@app.route('/new_inquilino', methods=['GET', 'POST'])
def new_inquilino():

    if request.method == 'POST':
        if not request.form['nome'] or not request.form['data_nascimento'] or not request.form['telefone']:
            flash('Please enter all the fields', 'error')
        else:
            inquilino = Inquilino(
                request.form['nome'], request.form['data_nascimento'], request.form['telefone'])

            db.session.add(inquilino)
            db.session.commit()
            flash('Inquilino cadastrado com sucesso!')
            return redirect(url_for('show_all_inquilinos'))
    return render_template('inquilino/new_inquilino.html')

@app.route('/inquilino/<id>', methods=['GET', 'POST'])
def update_inquilino(id):
    inquilino = Inquilino.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('inquilino/update_inquilino.html', inquilino=inquilino)

    if request.method == 'POST':
        inquilino.nome = request.form["nome"]
        inquilino.data_nascimento = request.form["data_nascimento"]
        inquilino.telefone = request.form["telefone"]

        db.session.add(inquilino)
        db.session.commit()

        flash('Inquilino atualizado com sucesso!')
        return redirect(url_for('show_all_inquilinos'))

@app.route('/inquilino_delete/<id>', methods=['GET', 'POST'])
def inquilino_delete(id):
    inquilino = Inquilino.query.get_or_404(id)
    print(id)
    
    if request.method == 'GET':
        return render_template('inquilino/delete_inquilino.html', inquilino=inquilino)
    if request.method == 'POST':
        if inquilino:
            try:
                db.session.delete(inquilino)
                db.session.commit()
                flash('Inquilino excluído com sucesso!')
                return redirect(url_for('show_all_inquilinos'))
            except IntegrityError:
                flash('Você não pode excluir esse inquilino por ele ser uma chave estrangeira!')
                return redirect(url_for('show_all_inquilinos'))
        abort(404)

# Proprietarios
@app.route('/show_all_proprietarios')
def show_all_proprietarios():
    return render_template('proprietario/show_all_proprietarios.html', proprietarios=Proprietario.query.all())

@app.route('/new_proprietario', methods=['GET', 'POST'])
def new_proprietario():

    if request.method == 'POST':
        if not request.form['nome'] or not request.form['data_nascimento'] or not request.form['telefone']:
            flash('Please enter all the fields', 'error')
        else:
            proprietario = Proprietario(
                request.form['nome'], request.form['data_nascimento'], request.form['telefone'])

            db.session.add(proprietario)
            db.session.commit()
            flash('Proprietário cadastrado com sucesso!')
            return redirect(url_for('show_all_proprietarios'))
    return render_template('proprietario/new_proprietario.html')

@app.route('/Proprietario/<id>', methods=['GET', 'POST'])
def update_proprietario(id):
    proprietario = Proprietario.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('proprietario/update_proprietario.html', proprietario=proprietario)

    if request.method == 'POST':
        proprietario.nome = request.form["nome"]
        proprietario.data_nascimento = request.form["data_nascimento"]
        proprietario.telefone = request.form["telefone"]

        db.session.add(proprietario)
        db.session.commit()

        flash('Proprietário atualizado com sucesso!')
        return redirect(url_for('show_all_proprietarios'))

@app.route('/proprietario_delete/<id>', methods=['GET', 'POST'])
def proprietario_delete(id):
    proprietario = Proprietario.query.get_or_404(id)
    print(id)
    if request.method == 'GET':
        return render_template('proprietario/delete_proprietario.html', proprietario=proprietario)
    if request.method == 'POST':
        if proprietario:
            try:
                db.session.delete(proprietario)
                db.session.commit()
                flash('Proprietário excluído com sucesso!')
                return redirect(url_for('show_all_proprietarios'))
            except IntegrityError:
                flash('Você não pode excluir esse proprietário por ele ser uma chave estrangeira!')
                return redirect(url_for('show_all_proprietarios'))
        abort(404)

# Corretor
@app.route('/show_all_corretores')
def show_all_corretores():
    return render_template('corretor/show_all_corretores.html', corretores=Corretor.query.all())

@app.route('/new_corretor', methods=['GET', 'POST'])
def new_corretor():

    if request.method == 'POST':
        if not request.form['nome'] or not request.form['data_nascimento'] or not request.form['telefone']:
            flash('Please enter all the fields', 'error')
        else:
            corretor = Corretor(
                request.form['nome'], request.form['data_nascimento'], request.form['telefone'])

            db.session.add(corretor)
            db.session.commit()
            flash('Corretor cadastrado com sucesso!')
            return redirect(url_for('show_all_corretores'))
    return render_template('corretor/new_corretor.html')

@app.route('/Corretor/<id>', methods=['GET', 'POST'])
def update_corretor(id):
    corretor = Corretor.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('corretor/update_corretor.html', corretor=corretor)

    if request.method == 'POST':
        corretor.nome = request.form["nome"]
        corretor.data_nascimento = request.form["data_nascimento"]
        corretor.telefone = request.form["telefone"]

        db.session.add(corretor)
        db.session.commit()

        flash('Corretor atualizado com sucesso!')
        return redirect(url_for('show_all_corretores'))

@app.route('/corretor_delete/<id>', methods=['GET', 'POST'])
def corretor_delete(id):
    corretor = Corretor.query.get_or_404(id)
    print(id)
    if request.method == 'GET':
        return render_template('corretor/delete_corretor.html', corretor=corretor)
    if request.method == 'POST':
        if corretor:
            try:
                db.session.delete(corretor)
                db.session.commit()
                flash('Corretor excluído com sucesso!')
                return redirect(url_for('show_all_corretores'))
            except IntegrityError:
                flash('Você não pode excluir esse corretor por ele ser uma chave estrangeira!')
                return redirect(url_for('show_all_corretores'))
        abort(404)

# Imovel
@app.route('/show_all_imoveis')
def show_all_imoveis():
    return render_template('imovel/show_all_imoveis.html', imoveis=Imovel.query.all())

@app.route('/new_imovel', methods=['GET', 'POST'])
def new_imovel():
    if request.method == 'POST':
        if not request.form['logradouro'] or not request.form['cep'] or not request.form['bairro'] or not request.form['cidade'] or not request.form['id_proprietario'] or not request.form['valor']:
            flash('Please enter all the fields', 'error')
        else:
            imovel = Imovel(request.form['logradouro'], request.form['cep'], request.form['bairro'],
                            request.form['cidade'], request.form['id_proprietario'], request.form['valor'])
            db.session.add(imovel)
            db.session.commit()
            flash('Imovel cadastrado com sucesso')
            return redirect(url_for('show_all_imoveis'))
    return render_template('imovel/new_imovel.html', proprietarios=Proprietario.query.all())

@app.route('/Imovel/<id>', methods=['GET', 'POST'])
def update_imovel(id):
    imovel = Imovel.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('imovel/update_imovel.html', imovel=imovel, proprietarios=Proprietario.query.all())

    if request.method == 'POST':
        imovel.logradouro = request.form["logradouro"]
        imovel.cep = request.form["cep"]
        imovel.cidade = request.form["cidade"]
        imovel.id_proprietario = request.form["id_proprietario"]
        imovel.valor = request.form["valor"]

        db.session.add(imovel)
        db.session.commit()

        flash('Imovel atualizado com sucesso')
        return redirect(url_for('show_all_imoveis'))

@app.route('/imovel_delete/<id>', methods=['GET', 'POST'])
def imovel_delete(id):
    imovel = Imovel.query.get_or_404(id)
    print(id)
    if request.method == 'GET':
        return render_template('imovel/delete_imovel.html', imovel=imovel)
    if request.method == 'POST':
        if imovel:
            try:
                db.session.delete(imovel)
                db.session.commit()
                flash('Imovel excluído com sucesso')
                return redirect(url_for('show_all_imoveis'))
            except IntegrityError:
                flash('Você não pode excluir esse imovel por ele ser uma chave estrangeira!')
                return redirect(url_for('show_all_imoveis'))
        abort(404)

# Aluguel
@app.route('/show_all_alugueis')
def show_all_alugueis():
    return render_template('aluguel/show_all_alugueis.html', alugueis=Aluguel.query.all())

@app.route('/new_aluguel', methods=['GET', 'POST'])
def new_aluguel():

    if request.method == 'POST':
        if not request.form['id_imovel'] or not request.form['id_inquilino'] or not request.form['id_corretor']:
            flash('Please enter all the fields', 'error')
        else:
            aluguel = Aluguel(
                request.form['id_imovel'], request.form['id_inquilino'], request.form['id_corretor'])

            db.session.add(aluguel)
            db.session.commit()
            flash('Aluguel cadastrado com sucesso')
            return redirect(url_for('show_all_alugueis'))
    return render_template('aluguel/new_aluguel.html', imoveis=Imovel.query.all(), inquilinos=Inquilino.query.all(), corretores=Corretor.query.all())

@app.route('/Aluguel/<id>', methods=['GET', 'POST'])
def update_aluguel(id):
    aluguel = Aluguel.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('aluguel/update_aluguel.html', aluguel=aluguel, imoveis=Imovel.query.all(), inquilinos=Inquilino.query.all(), corretores=Corretor.query.all())

    if request.method == 'POST':
        aluguel.id_imovel = request.form["id_imovel"]
        aluguel.id_inquilino = request.form["id_inquilino"]
        aluguel.id_corretor = request.form["id_corretor"]

        db.session.add(aluguel)
        db.session.commit()

        flash('Aluguel atualizado com sucesso')
        return redirect(url_for('show_all_alugueis'))

@app.route('/aluguel_delete/<id>', methods=['GET', 'POST'])
def aluguel_delete(id):
    aluguel = Aluguel.query.get_or_404(id)
    print(id)
    if request.method == 'GET':
        return render_template('aluguel/delete_aluguel.html', aluguel=aluguel)
    if request.method == 'POST':
        if aluguel:
            db.session.delete(aluguel)
            db.session.commit()
            flash('Aluguel excluído com sucesso')
            return redirect(url_for('show_all_alugueis'))
        abort(404)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
