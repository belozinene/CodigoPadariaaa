import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURAÇÃO ---
# Se for rodar no PyCharm, mude para: TOKEN = '8625088250:AAHFovlQ_1_oQZOTy-YrAdNJx7U5zA2kW9w'
# Se for mandar para o Railway, deixe como está abaixo:
TOKEN = os.getenv('TOKEN')

# Dicionário de produtos (Dica: use nomes sem acento para facilitar a digitação no dia a dia)
PRODUTOS = {
    "bolo ingles": "45",
"bolo abacaxi": "9165",
"bolo coco": "9167",
"bolo cenoura": "9173",
"bolo limão": "9168",
"bolo chocolate": "9171",
"pão de sal com queijo": "9350",
"pão milho": "221",
"farinha de rosca": "7455",
"torrada integral": "7608",
"torrada oregano": "9351",
"torrada especial": "4603",
"torrada tradicional": "7454",
"sonho creme": "1256",
"sonho doce de leite": "1259",
"mini sonho creme": "7812",
"mini sonho doce de leite": "7861",
"mini sonho goiabada": "7896",
"rabanada": "7928",
"brioche coco": "1026",
"brioche frutas": "7727",
"pão de leite kg": "7728",
"pão cachorro quente": "3498",
"pão hamburguer": "3496",
"pão hamburguer gergelim": "1023",
"pão brioche": "8616",
"pão mandioquinha": "8620",
"pão batata": "8610",
"pão de açucar": "24",
"pão de leite": "31",
"pão sovado": "548",
"pão doce coco": "36",
"pão doce creme": "1031",
"biscoito de queijo": "7230",
"broa milho": "2552",
"chipa / ferradura": "3289",
"palito de queijo": "3290",
"torta de frango": "3302",
"pão hamburguer balcão": "3301",
"esfirra": "3300",
"empadão": "3299",
"salgado frito un": "1445",
"salgado frito kg": "1447",
"donut doce de leite": "5410",
"donut fruta vermelha": "5411",
"donut creme": "5404",
"donut chocolate": "5406",
"donut com chocolate": "5408"
}


# Função de boas-vindas
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi! Digite o nome do produto e eu te mando o código da padaria. 🥐")


# Função que busca o código
async def buscar_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pega o texto, coloca em minúsculo e tira espaços sobrando
    texto_recebido = update.message.text.lower().strip()

    print(f"Buscando por: {texto_recebido}")  # Isso ajuda você a ver o que está acontecendo no log

    if texto_recebido in PRODUTOS:
        codigo = PRODUTOS[texto_recebido]
        await update.message.reply_text(f"✅ O código de {texto_recebido.upper()} é: {codigo}")
    else:
        # Se não encontrar, ele avisa e mostra o que tem cadastrado
        opcoes = ", ".join(PRODUTOS.keys())
        await update.message.reply_text(
            f"❌ Não encontrei '{texto_recebido}'.\n\n"
            f"Tente um destes: {opcoes}"
        )


def main():
    if not TOKEN:
        print("ERRO: O Token não foi encontrado! Verifique as variáveis de ambiente.")
        return

    # Cria o aplicativo do bot
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))

    # Respostas para mensagens de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_codigo))

    # Inicia o bot
    print("Bot rodando no Railway... (ou localmente)")
    application.run_polling()


if __name__ == '__main__':
    main()