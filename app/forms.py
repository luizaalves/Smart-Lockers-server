from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    """
    Formulário de login para o aplicativo Flask.

    Este formulário é utilizado para permitir a entrada de usuários autorizados no sistema,
    através das credenciais de login do usuário, incluindo o endereço de email e a senha. 
    Utiliza validações para garantir que ambos os campos sejam preenchidos antes de permitir a submissão.

    Atributos:
        email (StringField): Campo de entrada para o endereço de email do usuário.
                             Validação: Campo obrigatório.
        password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        submit (SubmitField): Botão de submissão do formulário.
    """
    email = StringField('User', validators=[DataRequired('Required field')])
    password = PasswordField('Password', validators=[DataRequired('Required field')])
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    """
    Formulário de registro para o aplicativo Flask.

    Este formulário é utilizado para cadastrar usuários novos no sistema, é necessário preencher
    obrigatoriamente todos os campos: nome, e-mail, senha e confirmação de senha.
    Após registrar, o usuário passa a ter acesso ao sistema.

    Atributos:
        name (StringField): Campo de entrada para o nome do usuário.
                             Validação: Campo obrigatório.
        email (StringField): Campo de entrada para o endereço de email do usuário.
                             Validação: Campo obrigatório.
        password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        confirm_password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        user_type (SelectField): Campo de seleção para o tipo de permissão que terá o usuário. [admin ou comum]
                                  Validação: Campo obrigatório.
        register (SubmitField): Botão de submissão do formulário.
    """
    nome = StringField('Nome', validators=[DataRequired('Campo obrigatório')])
    email = StringField('E-mail', validators=[DataRequired('Campo obrigatório'), Email('E-mail inválido')])
    senha = PasswordField('Senha', validators=[DataRequired('Campo obrigatório')])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired('Campo obrigatório'), EqualTo('senha', message='As senhas devem corresponder')])
    tipo_usuario = SelectField('Tipo de Usuário', choices=[('comum', 'Comum'), ('admin', 'Admin')], validators=[DataRequired('Campo obrigatório')])
    submit = SubmitField('Registrar')

class UpdateEmailPasswordForm(FlaskForm): # TODO: talvez eu possa unir os dois, mas o campo tipo de usuario eu deixar oculto se 
    """
    Formulário de atualização de senha para o aplicativo Flask.

    Este formulário é utilizado para atualizar as credenciais de senha do usuário que 
    está logado no sistema. O campo nome pode ser alterado, assim como o campo senha.

    Atributos:
        name (StringField): Campo de entrada para o nome do usuário.
                             Validação: Campo obrigatório.
        email (StringField): Campo de entrada para o endereço de email do usuário.
                             Validação: Campo obrigatório.
        password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        confirm_password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        submit (SubmitField): Botão de submissão do formulário.
    """
    #se for email de  quem fez  o login, autoriza
    nome = StringField('Nome', validators=[DataRequired('Campo obrigatório')])
    email = StringField('Novo Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem corresponder')])
    submit = SubmitField('Atualizar')

class UpdateEmailForm(FlaskForm):#TODO: Rever, pois se for pra atualizar as proprias credenciais, o campo tipo de usuario nao pode aparecer
    """
    Formulário de atualização de email para o aplicativo Flask.

    Este formulário é utilizado para atualizar as credenciais de e-mail qualquer usuário. 
    Deve aparecer somente para usuário do tipo admin. O campo nome pode ser alterado, 
    assim como o campo e-mail, desde que o campo old_email seja colocado corretamente. 

    Atributos:
        name (StringField): Campo de entrada para o nome do usuário.
                             Validação: Campo obrigatório.
        old_email (StringField): Campo de entrada para o endereço de e-mail atual do usuário.
                                  Validação: Campo obrigatório.
        email (StringField): Campo de entrada para o novo endereço de email do usuário.
                             Validação: Campo obrigatório.
        password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        user_type (SelectField): Campo de seleção para o tipo de permissão que terá o usuário. [admin ou comum]
                                  Validação: Campo obrigatório.
        submit (SubmitField): Botão de submissão do formulário.
    """
    #se for o login de um usuario admin, usa esse formulario, dai ele consegue atualizar qualquer usuario
    nome = StringField('Nome', validators=[DataRequired('Campo obrigatório')])
    old_email = StringField('Antigo Email', validators=[DataRequired()])
    email = StringField('Novo Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    tipo_usuario = SelectField('Tipo de Usuário', choices=[('comum', 'Comum'), ('admin', 'Admin')], validators=[DataRequired('Campo obrigatório')])
    submit = SubmitField('Atualizar')


class UpdatePasswordForm(FlaskForm):
    """
    Formulário de atualização de email e senha para o aplicativo Flask.
    
    Este formulário é utilizado para atualizar as credenciais de senha de qualquer usuário. 
    Deve aparecer somente para usuário do tipo admin. O campo nome pode ser alterado, 
    assim como o campo senha, desde que o campo email seja colocado corretamente. 

        Atributos:
        name (StringField): Campo de entrada para o nome do usuário.
                             Validação: Campo obrigatório.
        old_email (StringField): Campo de entrada para o endereço de e-mail atual do usuário.
                                  Validação: Campo obrigatório.
        email (StringField): Campo de entrada para o novo endereço de email do usuário.
                             Validação: Campo obrigatório.
        password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        confirm_password (PasswordField): Campo de entrada para a senha do usuário.
                                  Validação: Campo obrigatório.
        user_type (SelectField): Campo de seleção para o tipo de permissão que terá o usuário. [admin ou comum]
                                  Validação: Campo obrigatório.
        submit (SubmitField): Botão de submissão do formulário.
    """
    #se for o login de um usuario admin, usa esse formulario, dai ele consegue atualizar qualquer usuario
    nome = StringField('Nome', validators=[DataRequired('Campo obrigatório')])
    email = StringField('Email', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem corresponder')])
    tipo_usuario = SelectField('Tipo de Usuário', choices=[('comum', 'Comum'), ('admin', 'Admin')], validators=[DataRequired('Campo obrigatório')])
    submit = SubmitField('Atualizar')
