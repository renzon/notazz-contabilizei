# notazz-contabilizei
Projeto para automatizar importação de XML do Notazz no Contabilzei

## Como usar

Baixe o projeto

Instala o Python 3.7 e o pipenv

Na raiz do projeto, rode:

`pipenv sync`

Na raiz do projeto crie um arquivo chamado `.env` com o seguinte formato:

```
CONTABILIZEI_USERNAME=seu usuario no contabilizei
CONTABILIZEI_PASSWORD=sua senha no contabilizei
```

Para valores vc deve colocar o seu username e senha do contabilizei

Feito isso, acesse o [https://notajoseense.sjc.sp.gov.br/notafiscal/paginas/portal/login.html#](sistema de notas da prefeitura)

Gere a RPS do período de notas que quer importar, baixe o arquivo xml

Crie no projeto um diretório chamado 'in', copie o arquivo xml que baixou para dentro dele

No projeto, rode `pipenv run python main.py`

##Obs

As vezes programa pode falhar para algumas notas, mas ele vai imprimindo as que foram processadas.
Assim quando ouve falhas eu simplesmente editei o cml para tirar as já processadas,
Consertei a possível nota com problema e reiniciei o processamento

