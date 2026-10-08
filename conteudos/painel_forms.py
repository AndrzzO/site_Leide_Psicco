from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.utils.html import strip_tags
from .models import Artigo, CategoriaArtigo
from .sanitizacao import sanitizar_editor


class LoginProprietariaForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail', max_length=150, widget=forms.EmailInput(attrs={'autocomplete': 'username', 'autofocus': True}))
    password = forms.CharField(label='Senha', max_length=256, strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    error_messages = {'invalid_login': 'E-mail ou senha incorretos.', 'inactive': 'E-mail ou senha incorretos.'}

    def clean_username(self):
        return self.cleaned_data['username'].strip().lower()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.has_perm('conteudos.gerenciar_blog'):
            raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')


class ArtigoEditorForm(forms.ModelForm):
    capa_x = forms.IntegerField(required=False, min_value=0, max_value=100, widget=forms.HiddenInput())
    capa_y = forms.IntegerField(required=False, min_value=0, max_value=100, widget=forms.HiddenInput())
    permanencia = forms.ChoiceField(label='Permanência', choices=[('permanente', 'Permanente'), ('temporario', 'Apagar em uma data')])
    apagar_em = forms.DateTimeField(label='Data e horário da exclusão', required=False,
        input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}))
    conteudo = forms.CharField(label='Texto', max_length=100000, widget=forms.Textarea(attrs={'rows': 16}))
    resumo = forms.CharField(label='Apresentação breve', max_length=500, required=False, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Artigo
        fields = ['titulo', 'resumo', 'categoria', 'fonte', 'conteudo', 'imagem_capa', 'capa_x', 'capa_y', 'texto_alternativo_imagem', 'apagar_em']
        labels = {'titulo': 'Título', 'fonte': 'Fonte do texto', 'imagem_capa': 'Foto de capa (opcional)', 'texto_alternativo_imagem': 'Descrição da foto'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriaArtigo.objects.filter(ativo=True)
        self.initial['permanencia'] = 'temporario' if self.instance.apagar_em else 'permanente'
        if self.instance.pk:
            self.initial['conteudo'] = self.instance.conteudo_formatado

    def clean_conteudo(self):
        texto = sanitizar_editor(self.cleaned_data['conteudo'])
        if not strip_tags(texto).strip():
            raise forms.ValidationError('Escreva o texto do artigo antes de salvar.')
        return texto

    def clean(self):
        dados = super().clean()
        for eixo in ('capa_x', 'capa_y'):
            if eixo not in self.errors and dados.get(eixo) is None:
                dados[eixo] = getattr(self.instance, eixo, 50)
        if dados.get('permanencia') == 'permanente':
            dados['apagar_em'] = None
        elif not dados.get('apagar_em') or dados['apagar_em'] <= timezone.now():
            self.add_error('apagar_em', 'Escolha uma data e horário no futuro (horário de Brasília).')
        if dados.get('imagem_capa') and not dados.get('texto_alternativo_imagem'):
            self.add_error('texto_alternativo_imagem', 'Descreva a foto para quem utiliza leitor de tela.')
        return dados
