import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from rapidfuzz import process, utils
from unidecode import unidecode

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv("TOKEN")

# Sua lista de produtos (mantive exatamente como você mandou)
PRODUTOS = {
    "BOLO DE MILHO": "8643",
    "BOLO NEGA MALUCA": "9187",
    "BOLO ABACAXI": "5492",
    "BOLO BANANA": "3149",
    "BOLO LIMÃO": "9168",
    "BOLO LIMAO C/ COBERTURA": "9180",
    "BOLO COCO": "9167",
    "BOLO COCO COM COBERTURA": "9178",
    "BOLO CENOURA": "9173",
    "BOLO CENOURA C/ COBERTURA": "9186",
    "BOLO CHURROS": "9200",
    "BOLO FORMIGUEIRO": "1228",
    "BOLO MAÇA": "5492",
    "BOLO LARANJA": "9169",
    "BOLO FUBÁ": "9170",
    "BOLO CHOCOLATE": "9171",
    "CAKE MULTI CEREAIS": "8639",
    "CAKE TRADICIONAL": "8641",
    "CAKE RED VELT": "9183",
    "TORTELA DE MORANGO": "80",
    "TORTELETE DE LIMÃO": "958",
    "TORTA CHOCOLATE": "8299",
    "TORTA DOCE DE LEITE": "8425",
    "TORTA CHOC MORANGO": "8434",
    "TORTA LEITE EM PÓ": "8310",
    "TORTA LEITE EM PÓ COM MORANGO": "8314",
    "TORTA BRIGADEIRO": "8316",
    "TORTA MESCLADA": "8306",
    "BRIGADEIRO": "74",
    "BEIJINHO": "89",
    "PANACOTA MORANGO": "8672",
    "PANACOTA UVA": "8896",
    "COPO DA FELICIDADE": "990",
    "PÃO CIABATA": "8618",
    "PÃO AUSTRALIANO": "8613",
    "PÃO SOVADO": "548",
    "PÃO LEITE": "31",
    "PÃO INTEGRAL": "30",
    "PÃO MANDIOQUINHA": "8620",
    "PÃO DE OVOS": "23",
    "PÃO HAMBÚRGUER": "3496",
    "PÃO HAMBÚRGUER GERGELIM": "1023",
    "COSTELA DE ADÃO": "11673",
    "COXINHA DE FRANGO": "11677",
    "COXINHA COM CATUPIRI": "116778",
    "CROISSANT": "11675",
    "EMPADA DE FRANGO": "11670",
    "ENROLADINHO ASSADO UNI": "11674",
    "ENROLADINHO FRITO": "11679",
    "ESFIRRA": "11666",
    "KIBE RECHEADO CARNE FRITO": "11672",
    "NAPOLITANO": "11668",
    "PÃO BATATA": "11669",
    "PÃO HAMBÚRGUER UN": "11667",
    "SALGADINHOS FRITOS": "1447",
    "COXINHA PADARIA": "10473",
    "BISCOITO CASEIRO": "7230",
    "BISCOITO PALITO": "3290",
    "PÃO QUEIJO": "1229",
    "CHIPA": "3289",
    "PÃO HOT DOG KG": "3498",
    "PUDIM DE LEITE KG": "1217",
    "BEUINHO KG": "39",
    "BROA DE MILHO KG": "2552",
    "BRIGADEIRO KG": "74",
    "PÃO BRIOCHE KG": "8636",
    "SUSPIRO KG": "2727",
    "CHOCOTONE": "1309",
    "PÃO BATATA KG": "8610",
    "TORTA DE FRANGO": "3302",
    "PANETONE FRUTAS": "1312",
    "PÃO DE MILHO KG": "221",
    "PÃO HAMBURGUER": "3301",
    "PANETONE SALGADO": "7620",
    "PÃO DE AÇUCAR KG": "24",
    "PANETONE BRIGADEIRO": "1306",
    "EMPADÃO": "3299",
    "PAMONHA": "844853",
    "SALGADO FRITO": "1445",
    "PÃO CASEIRINHO KG": "8633",
    "PÃO DOCE COCO KG": "36",
    "PÃO MINUTO KG": "21",
    "BROA ROCA KG": "8642",
    "PÃO DOCE CREME KG": "1031",
    "COXINHA MÉDIA": "13204",
    "MANJAR": "9913",
    "PALHA ITALIANA": "9915",
    "GELATINA COLORIDA": "2022",
    "MARIA MOLE": "302",
    "DONUTS DOCE DE LEITE": "5410",
    "DONUTS FRUTAS VERMELHAS": "5411",
    "DONUTS CREME": "5404",
    "DONUTS CHOCOLATE": "5406",
    "DONUTS COBERTURA C/ CHOC": "5408",
    "RING FRUTAS VERMELHAS": "6997",
    "RING CHOCOLATE": "6998",
    "RING DOCE DE LEITE": "7002",
    "SONHO CREME": "1259",
    "SONHO DOCE DE LEITE": "8720",
    "SONHO CHOCOLATE": "8720",
    "MINI SONHO CREME": "7812",
    "MINI SONHO DOCE DE LEITE": "7861",
    "MINI SONHO GOIABADA": "7896",
    "LUA MEL": "8764",
    "PÃO DOCE CREME": "7726",
    "PÃO DOCE COCO": "7725",
    "BRIOCHE COCO": "1026",
    "BRIOCHE FRUTAS": "7727",
    "BRIOCHE CHOCOLATE": "6483",
    "PÃO CUCA": "1798",
    "FATIA HUNGARA": "7927",
    "PÃO DOCE GOIABA": "552",
    "ROSCA CREME COM COCO": "5487",
}

# Criamos uma versão "limpa" (sem acento) da lista para o bot comparar melhor
PRODUTOS_LIMPOS = {unidecode(k).lower(): k for k in PRODUTOS.keys()}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi! Digite o nome do produto e eu te mando o código. 🥐")


async def buscar_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Limpa o texto que você enviou (sem acento e minúsculo)
    entrada_usuario = unidecode(update.message.text.lower().strip())

    # 2. Procura a melhor combinação na nossa lista limpa
    # O "score_cutoff=60" faz ele ignorar se a palavra for muito nada a ver
    resultado = process.extractOne(
        entrada_usuario,
        PRODUTOS_LIMPOS.keys(),
        processor=utils.default_process,
        score_cutoff=60
    )

    if resultado:
        nome_limpo_encontrado = resultado[0]
        nome_original = PRODUTOS_LIMPOS[nome_limpo_encontrado]
        codigo = PRODUTOS[nome_original]

        await update.message.reply_text(f"✅ {nome_original}: {codigo}")
    else:
        # Se ele não tiver 60% de certeza, ele manda essa mensagem curta
        await update.message.reply_text("❌ Não encontrei. Tente digitar o nome de outro jeito!")


def main():
    if not TOKEN:
        print("ERRO: Token não encontrado!")
        return

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_codigo))

    print("Bot inteligente rodando...")
    application.run_polling()


if __name__ == '__main__':
    main()