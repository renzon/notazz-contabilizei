from collections import namedtuple
from decimal import Decimal
from os import path, walk

import xmltodict

_PROJECT_IN_PATH = path.dirname(__file__)
_PROJECT_IN_PATH = path.join(_PROJECT_IN_PATH, 'in')

Endereco = namedtuple('Endereco', 'logradouro numero complemento bairro cep')
Servico = namedtuple('Servico', 'valor descricao')


class Nota:
    def __init__(self, numero: str, data_emissao: str, competencia: str, cpf_cnpj: str, razao_social: str,
                 endereco: Endereco, servico: Servico):
        self.servico = servico
        self.endereco = endereco
        self.razao_social = razao_social
        self.cpf_cnpj = cpf_cnpj
        self.competencia = competencia
        self.data_emissao = data_emissao
        self.numero = numero

    @property
    def tipo_cliente(self):
        if len(self.cpf_cnpj) == 11:
            return 'tipo-cliente-PF'
        return 'tipo-cliente-PJ'


def to_br_data(dt: str) -> str:
    year, month, day = dt.split('-')
    return f'{day}/{month}/{year}'


def process_xml_files(xml_dir_path=_PROJECT_IN_PATH):
    for _, _, file_names in walk(xml_dir_path):
        for file_name in file_names:
            file_path = path.join(xml_dir_path, file_name)
            with open(file_path, 'rb') as xml_file:
                dct = xmltodict.parse(xml_file)
                notas = dct['ListaNotaFiscal']['Nfse']
                for nfse in notas:
                    nota_inf = nfse['InfNfse']
                    tomador = nota_inf['TomadorServico']
                    endereco_dct = tomador['Endereco']
                    try:
                        cep = endereco_dct['Cep']
                        cep = ('0' * (8 - len(cep))) + cep
                        endereco = Endereco(
                            endereco_dct['Endereco'],
                            endereco_dct['Numero'],
                            endereco_dct.get('Complemento', ''),
                            endereco_dct['Bairro'],
                            cep,
                        )
                    except KeyError:
                        continue
                    servico_dct = nota_inf['Servico']
                    valor = Decimal(servico_dct['Valores']['ValorServicos'])
                    valor_em_centavos = f'{valor:.2f}'.replace('.', '')
                    servico = Servico(valor_em_centavos, servico_dct['Discriminacao'])
                    cpf_or_cnpj = tomador['IdentificacaoTomador']['CpfCnpj']
                    yield Nota(
                        nota_inf['Numero'],
                        to_br_data(nota_inf['DataEmissao'][:10]),
                        to_br_data(nota_inf['Competencia'][:10]),
                        cpf_or_cnpj.get('Cpf', cpf_or_cnpj.get('Cnpj')),
                        tomador['RazaoSocial'],
                        endereco,
                        servico
                    )


if __name__ == '__main__':
    nota = list(process_xml_files())
    print(nota)
