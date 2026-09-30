"""
Formulários do app contato.
Implementa ContatoForm com minimização de dados, validação server-side de canal de retorno,
proteção contra bots (honeypot) e respeito ao Design System.
"""
import re
from django import forms
from servicos.models import Servico
from .models import MensagemContato


class ContatoForm(forms.ModelForm):
    """
    Formulário seguro de contato institucional.
    Exige Nome e ao menos um meio de retorno (E-mail OU Telefone/WhatsApp),
    com consentimento obrigatório da Política de Privacidade e proteção contra spam.
    """
    # Campo armadilha honeypot invisível para usuários humanos
    campo_verificacao = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'aria-hidden': 'true',
            'style': 'display:none !important; position:absolute; left:-9999px; visibility:hidden;',
        })
    )

    class Meta:
        model = MensagemContato
        fields = [
            'nome',
            'email',
            'telefone',
            'servico_interesse',
            'mensagem',
            'aceite_privacidade',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'autocomplete': 'name',
                'placeholder': 'Seu nome completo',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'autocomplete': 'email',
                'placeholder': 'seuemail@exemplo.com.br',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-input',
                'autocomplete': 'tel',
                'inputmode': 'tel',
                'placeholder': '(61) 99999-9999',
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 5,
                'maxlength': '2000',
                'placeholder': 'Escreva uma mensagem breve sobre sua dúvida ou atendimento desejado...',
            }),
            'aceite_privacidade': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
                'required': 'required',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_spam = False

        # Configura queryset dinâmico dos serviços ativos
        self.fields['servico_interesse'].queryset = Servico.objects.filter(ativo=True).order_by('ordem', 'nome')
        self.fields['servico_interesse'].empty_label = "Selecione um serviço ou tema (opcional)"
        self.fields['servico_interesse'].widget.attrs.update({'class': 'form-select'})

        # Ajusta obrigatoriedade de campos conforme regra de contato alternativo e acessibilidade WCAG
        self.fields['nome'].required = True
        self.fields['nome'].widget.attrs['aria-required'] = 'true'
        self.fields['email'].required = False
        self.fields['telefone'].required = False
        self.fields['mensagem'].required = False
        self.fields['aceite_privacidade'].required = True
        self.fields['aceite_privacidade'].widget.attrs['aria-required'] = 'true'

    def full_clean(self):
        super().full_clean()
        for field_name in self.errors:
            if field_name in self.fields:
                widget = self.fields[field_name].widget
                widget.attrs['aria-invalid'] = 'true'
                widget.attrs['aria-describedby'] = f"id_{field_name}-erro"

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 2:
            raise forms.ValidationError("Por favor, informe seu nome com pelo menos 2 caracteres.")
        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()
        if telefone:
            # Extrai apenas os dígitos para validação de comprimento razoável
            digitos = re.sub(r'\D', '', telefone)
            if len(digitos) < 8 or len(digitos) > 15:
                raise forms.ValidationError(
                    "Por favor, informe um número de telefone com DDD válido (entre 8 e 15 dígitos)."
                )
        return telefone

    def clean_mensagem(self):
        mensagem = self.cleaned_data.get('mensagem', '').strip()
        if len(mensagem) > 2000:
            raise forms.ValidationError("A mensagem não pode ultrapassar 2000 caracteres.")
        return mensagem

    def clean_aceite_privacidade(self):
        aceite = self.cleaned_data.get('aceite_privacidade')
        if not aceite:
            raise forms.ValidationError(
                "É obrigatório declarar ciência da Política de Privacidade para enviar a mensagem."
            )
        return aceite

    def clean(self):
        cleaned_data = super().clean()

        # Detecção de bot via Honeypot
        campo_bot = cleaned_data.get('campo_verificacao')
        if campo_bot:
            self.is_spam = True

        # Validação cruzada: E-mail OU Telefone deve ser fornecido
        email = cleaned_data.get('email', '')
        telefone = cleaned_data.get('telefone', '')

        if not email and not telefone:
            msg_erro = "Por favor, informe ao menos um meio de contato (e-mail ou telefone/WhatsApp) para que possamos responder."
            self.add_error('email', msg_erro)
            self.add_error('telefone', msg_erro)

        return cleaned_data
