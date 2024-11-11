from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class ResetPasswordForm(FlaskForm):
    """
    Formulário para redefinição de senha.

    Este formulário é utilizado para que o usuário possa redefinir sua senha após ter recebido
    um link ou código de recuperação. O campo de email é exibido como somente leitura para
    assegurar que o usuário não o modifique.

    Atributos:
        email (StringField): Campo de entrada para o endereço de email do usuário.
                             Este campo é somente leitura para evitar modificações.
        new_password (PasswordField): Campo de entrada para a nova senha.
                                      Validação: O campo é obrigatório.
        confirm_password (PasswordField): Campo de entrada para confirmar a nova senha.
                                          Validação: O campo é obrigatório e deve corresponder ao valor de 'new_password'.
        submit (SubmitField): Botão para enviar e confirmar a nova senha definida.
    """
    email = StringField('Email', render_kw={'readonly': True})
    new_password = PasswordField('Nova Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('new_password', message='As senhas devem corresponder.')])
    submit = SubmitField('Enviar')

class ForgotPasswordForm(FlaskForm):
    """
    Formulário para recuperação de senha.

    Este formulário é utilizado para permitir que o usuário solicite um link de redefinição de senha
    ou insira um código de recuperação, caso já tenha recebido um, para redefinir sua senha.

    Atributos:
        email (StringField): Campo de entrada para o endereço de email do usuário.
                             Validação: O campo é obrigatório e deve ser um endereço de email válido.
        submit (SubmitField): Botão para enviar o link de redefinição de senha para o email fornecido.
        link (SubmitField): Botão para permitir ao usuário indicar que já possui um link de redefinição de senha.
        code (StringField): Campo de entrada para o código de recuperação enviado ao usuário.
                            Este campo é opcional e deve ser preenchido caso o usuário escolha validar um código.
        submit_code (SubmitField): Botão para validar o código de recuperação inserido no campo 'code'.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar link de redefinição')
    link = SubmitField('Já possuo link de redefinição')
    code = StringField('Código')
    submit_code = SubmitField('Validar')

class CompartmentAdmin(FlaskForm):
    """
    Formulário para admin se associar a qualquer compartimento em uso.

    Este formulário é utilizado para trocar ou atualizar informações sobre o compartimento
    e o nome do armário ao qual ele pertence no sistema de gerenciamento de lockers.

    Atributos:
        compartment (StringField): Campo de entrada para o identificador ou nome do compartimento.
        locker_name (StringField): Campo de entrada para o nome do armário ao qual o compartimento pertence.
        submit (SubmitField): Botão de submissão para confirmar a troca ou atualização de dados.
    """
    compartment = StringField('Compartment')#TODO obrigatorio
    locker_name = StringField('Locker name')
    submit = SubmitField('Trocar')

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
    forgot_password = SubmitField('Forgot password')

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
    tag = StringField('Tag', validators=[DataRequired('Campo obrigatório')])
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
    nome = StringField('Nome', validators=[DataRequired('Campo obrigatório')])
    tag = StringField('Tag', validators=[DataRequired('Campo obrigatório')])
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
