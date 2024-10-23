from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_session' 

@app.route('/', methods=['GET', 'POST'])
def registro():
    if 'inscritos' not in session:
        session['inscritos'] = []

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        turno = request.form.get('turno')
        seminarios = ', '.join(request.form.getlist('seminarios'))

        nuevo_inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios
        }
        session['inscritos'].append(nuevo_inscrito)
        session.modified = True 

        return redirect(url_for('lista'))

    return render_template('registro.html')

@app.route('/lista')
def lista():
    inscritos = session.get('inscritos', [])
    return render_template('lista.html', inscritos=inscritos)

@app.route('/eliminar/<int:index>')
def eliminar(index):
    session['inscritos'].pop(index)
    session.modified = True  
    return redirect(url_for('lista'))

@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    if request.method == 'POST':
        session['inscritos'][index] = {
            'fecha': request.form.get('fecha'),
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'turno': request.form.get('turno'),
            'seminarios': ', '.join(request.form.getlist('seminarios'))
        }
        session.modified = True
        return redirect(url_for('lista'))

    inscrito = session['inscritos'][index]
    return render_template('editar.html', inscrito=inscrito, index=index)

if __name__ == '__main__':
    app.run(debug=True)
