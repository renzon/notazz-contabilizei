import sys
from time import sleep

from decouple import config
from splinter import Browser

from xml_reader import process_xml_files

username = config('CONTABILIZEI_USERNAME')
password = config('CONTABILIZEI_PASSWORD')
with Browser('chrome', executable_path='./chromedriver') as browser:
    browser.visit('https://app.contabilizei.com.br')
    browser.find_by_id('user').fill(username)
    browser.find_by_id('password').fill(password)
    browser.find_by_css('.login-btn').click()
    sleep(8)  # Give time to run
    browser.visit('https://app.contabilizei.com.br/sistema/#/registrarnota')
    for nota in process_xml_files():
        browser.reload()
        sleep(8)  # Give time to run
        browser.find_by_css('input[name="Data de emissão"]').fill(nota.data_emissao)
        browser.find_by_css('input[name="Número"]').fill(nota.numero)
        browser.find_by_id('dataCompetencia').fill(nota.competencia)
        btn_novo_client = browser.find_by_id('btnNovoCliente')
        btn_novo_client.click()
        tipo_cliente = nota.tipo_cliente
        browser.find_by_css(f'input[name="{tipo_cliente}"]').click()
        sleep(1)
        browser.find_by_css('input[ng-model="nota.nomeRazaoTomador"]').fill(nota.razao_social)
        if tipo_cliente == 'tipo-cliente-PF':
            browser.find_by_css('input[name="CPF"]').fill(nota.cpf_cnpj)
        else:
            browser.find_by_css('input[name="CNPJ"]').fill(nota.cpf_cnpj)
        browser.find_by_css('input[name="CEP"]').fill(nota.endereco.cep)
        browser.find_by_css('button[ng-disabled="carregandoCep"]').click()
        sleep(4)  # Give time to run
        browser.find_by_css('input[ng-model="nota.logradouroEnderecoTomador"]').fill(nota.endereco.logradouro)
        browser.find_by_css('input[ng-model="nota.numeroEnderecoTomador"]').fill(nota.endereco.numero)
        browser.find_by_css('input[ng-model="nota.complementoEnderecoTomador"]').fill(nota.endereco.complemento)
        browser.find_by_css('input[ng-model="nota.bairroEnderecoTomador"]').fill(nota.endereco.bairro)
        browser.find_by_id('btnExibeDadosServico').click()
        sleep(2)  # Give time to run
        browser.find_by_css('textarea[ng-model="nota.discriminacao"]').fill(nota.servico.descricao)
        browser.find_by_css('input[ng-model="nota.valorServico"]').fill(nota.servico.valor)
        browser.find_by_id('btnEmitir').click()
        sleep(2)  # Give time to run
        browser.find_by_css('button[ng-class="btn.cssClass"]').click()
        sleep(8)  # Give time to run

        print(f'processada nota: {nota.numero}')
