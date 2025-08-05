# Import do Web Bot
from botcity.web import WebBot, Browser, By
from webdriver_manager.firefox import GeckoDriverManager

# Import de integração com BotCity Maestro SDK
from botcity.maestro import BotMaestroSDK, AutomationTaskFinishStatus, AlertType

# Desabilita erros enquanto não tem conexão com Orquestrador (para execução local)
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Instancia do SDK + autenticação
    maestro = BotMaestroSDK.from_sys_args()
    ## Obtém detalhes de uma tarefa
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    # Instancia do Web Bot
    bot = WebBot()

    # Configuração do Navegador
    bot.headless = False
    bot.browser = Browser.FIREFOX
    bot.driver_path = GeckoDriverManager().install()

    maestro.alert(
        task_id=execution.task_id,
        title="Começando processo",
        message="This is an info alert",
        alert_type=AlertType.INFO
    )

    # Abre website.
    bot.browse("https://practicetestautomation.com/practice-test-login/")
    
    # Busca pelo elemento input de nome de usuário
    elemento_campo_usuario = bot.find_element(
        selector="username",
        by=By.ID
        )
    # Ação de digitar no elemento, valor vindo de credenciais
    elemento_campo_usuario.send_keys(maestro.get_credential(label="cofre-login", key="user"))

    # Busca pelo elemento input de senha
    elemento_campo_senha = bot.find_element(
        selector="password",
        by=By.ID
        )
    # Ação de digitar no elemento, valor vindo de credenciais
    elemento_campo_senha.send_keys(maestro.get_credential(label="cofre-login", key="password"))

    # Busca pelo elemento botão submit
    elemento_botao = bot.find_element(
        selector="submit",
        by=By.ID
        )
    # Ação de clicar
    elemento_botao.click()

    bot.wait(5000)

    try:
        # Busca pela confirmação de login
        elemento_logado = bot.find_element(
            selector=".post-title",
            by=By.CSS_SELECTOR
            )
        # Imprime o texto da confirmação
        print(elemento_logado.text)

        # Busca pelo elemento botão log out
        elemento_deslogado = bot.find_element(
            selector=".wp-block-button__link",
            by=By.CSS_SELECTOR
            )
        # Ação de clicar no elemento
        elemento_deslogado.click()


    except Exception:
        # Busca pelo elemento de mensagem de erro
        error_alert = bot.find_element(
            selector="error",
            by=By.ID
            )

        # Imprime a mensagem de erro
        print(error_alert.text)

    finally:
        # Finaliza fechando o navegador
        bot.stop_browser()

        # Imprime mensagem de finalização
        print("Finally")
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="Tarefa foi concluída com sucesso.",
            total_items=1, # Número total de itens processados
            processed_items=1, # Número de itens processados com sucesso
            failed_items=0 # Número de itens processados com falha
        )



def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
