@echo off
echo Criando estrutura de diretórios para Token Counter Pro...

REM Criar a pasta principal do projeto
mkdir token_counter_pro

REM Criar subdiretórios
mkdir token_counter_pro\core
mkdir token_counter_pro\ui
mkdir token_counter_pro\cli

REM Criar arquivos init.py vazios
type nul > token_counter_pro\core_init_.py
type nul > token_counter_pro\ui_init_.py
type nul > token_counter_pro\cli_init_.py

REM Criar arquivos principais (vazios por enquanto)
type nul > token_counter_pro\core\counter.py
type nul > token_counter_pro\core\scanner.py
type nul > token_counter_pro\ui\app.py
type nul > token_counter_pro\ui\frame.py
type nul > token_counter_pro\cli\interface.py
type nul > token_counter_pro\main.py

echo Estrutura criada com sucesso!
echo Por favor, comece a preencher os arquivos com o código.
@echo on