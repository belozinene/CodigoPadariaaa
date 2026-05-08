from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURAÇÃO ---
TOKEN = '8625088250:AAHFovlQ_1_oQZOTy-YrAdNJx7U5zA2kW9w'

# Aqui você cadastra os produtos da sua padaria
# Chave: Nome que você vai digitar | Valor: O código do produto
PRODUTOS = {
    "pão francês": "101",
    "pão de queijo": "205",
    "sonho": "310",
    "focaccia": "415",
    "pão de sal": "101",  # Você pode ter apelidos para o mesmo código
}


# Função de boas-vindas
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi! Digite o nome do produto e eu te mando o código da padaria. 🥐")


# Função que busca o código
async def buscar_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_recebido = update.message.text.lower().strip()

    if texto_recebido in PRODUTOS:
        codigo = PRODUTOS[texto_recebido]
        await update.message.reply_text(f"O código de {texto_recebido.upper()} é: {codigo}")
    else:
        await update.message.reply_text("Produto não encontrado. Verifique se escreveu certinho!")


def main():
    # Cria o aplicativo do bot
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))

    # Respostas para mensagens de texto comuns
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_codigo))

    # Inicia o bot
    print("Bot rodando... Pressione Ctrl+C para parar.")
    application.run_polling()


if __name__ == '__main__':
    main()