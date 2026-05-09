import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from unidecode import unidecode

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv("TOKEN")

# Sua lista de produtos
PRODUTOS = {
  "BEIJINHO": "89",
  "BEUINHO KG": "39",
  "BISCOITO CASEIRO": "7230",
  "BISCOITO DE QUEIJO": "7230",
  "BISCOITO PALITO": "3290",
  "BOLO ABACAXI": "5492",
  "BOLO BANANA": "3149",
  "BOLO CENOURA": "9173",
  "BOLO CENOURA C/ COBERTURA": "9186",
  "BOLO CHOCOLATE": "9171",
  "BOLO CHURROS": "9200",
  "BOLO COCO": "9167",
  "BOLO COCO COM COBERTURA": "9178",
  "BOLO DE MILHO": "8643",
  "BOLO FORMIGUEIRO": "1228",
  "BOLO FUBÁ": "9170",
  "BOLO LARANJA": "9169",
  "BOLO LIMÃO": "9168",
  "BOLO LIMAO C/ COBERTURA": "9180",
  "BOLO MAÇA": "5492",
  "BOLO NEGA MALUCA": "9187",
  "BRIGADEIRO": "74",
  "BRIGADEIRO KG": "74",
  "BRIOCHE CHOCOLATE": "6483",
  "BRIOCHE COCO": "1026",
  "BRIOCHE FRUTAS": "7727",
  "BROA DE MILHO KG": "2552",
  "BROA ROCA KG": "8642",
  "CAKE MULTI CEREAIS": "8639",
  "CAKE RED VELT": "9183",
  "CAKE TRADICIONAL": "8641",
  "CHIPA": "3289",
  "CHOCOTONE": "1309",
  "COPO DA FELICIDADE": "990",
  "COSTELA DE ADÃO": "11673",
  "COXINHA COM CATUPIRI": "116778",
  "COXINHA DE FRANGO": "11677",
  "COXINHA MÉDIA": "13204",
  "COXINHA PADARIA": "10473",
  "CROISSANT": "11675",
  "DONUTS CHOCOLATE": "5406",
  "DONUTS COBERTURA C/ CHOC": "5408",
  "DONUTS CREME": "5404",
  "DONUTS DOCE DE LEITE": "5410",
  "DONUTS FRUTAS VERMELHAS": "5411",
  "EMPADA DE FRANGO": "11670",
  "EMPADÃO": "3299",
  "ENROLADINHO ASSADO UNI": "11674",
  "ENROLADINHO FRITO": "11679",
  "ESFIRRA": "11666",
  "FATIA HUNGARA": "7927",
  "GELATINA COLORIDA": "2022",
  "KIBE RECHEADO CARNE FRITO": "11672",
  "LUA MEL": "8764",
  "MANJAR": "9913",
  "MARIA MOLE": "302",
  "MINI SONHO CREME": "7812",
  "MINI SONHO DOCE DE LEITE": "7861",
  "MINI SONHO GOIABADA": "7896",
  "NAPOLITANO": "11668",
  "PALHA ITALIANA": "9915",
  "PAMONHA": "844853",
  "PANACOTA MORANGO": "8672",
  "PANACOTA UVA": "8896",
  "PANETONE BRIGADEIRO": "1306",
  "PANETONE FRUTAS": "1312",
  "PANETONE SALGADO": "7620",
  "PÃO AUSTRALIANO": "8613",
  "PÃO BATATA": "11669",
  "PÃO BATATA KG": "8610",
  "PÃO BRIOCHE KG": "8636",
  "PÃO CASEIRINHO KG": "8633",
  "PÃO CIABATA": "8618",
  "PÃO CUCA": "1798",
  "PÃO DE AÇUCAR KG": "24",
  "PÃO DE MILHO KG": "221",
  "PÃO DE OVOS": "23",
  "PÃO DOCE COCO": "7725",
  "PÃO DOCE COCO KG": "36",
  "PÃO DOCE CREME": "7726",
  "PÃO DOCE CREME KG": "1031",
  "PÃO DOCE GOIABA": "552",
  "PÃO HAMBÚRGUER": "3496",
  "PÃO HAMBÚRGUER GERGELIM": "1023",
  "PÃO HAMBÚRGUER UN": "11667",
  "PÃO HAMBURGUER": "3301",
  "PÃO HOT DOG KG": "3498",
  "PÃO INTEGRAL": "30",
  "PÃO DE LEITE": "31",
  "PÃO MANDIOQUINHA": "8620",
  "PÃO MINUTO KG": "21",
  "PÃO DE QUEIJO": "1229",
  "PÃO DE QUEIJO COM GOIABADA": "12392",
  "PÃO SOVADO": "548",
  "PUDIM DE LEITE KG": "1217",
  "RING CHOCOLATE": "6998",
  "RING DOCE DE LEITE": "7002",
  "RING FRUTAS VERMELHAS": "6997",
  "ROSCA CREME COM COCO": "5487",
  "SALGADINHOS FRITOS": "1447",
  "SALGADO FRITO": "1445",
  "SONHO CHOCOLATE": "8720",
  "SONHO CREME": "1259",
  "SONHO DOCE DE LEITE": "8720",
  "SUSPIRO KG": "2727",
  "TORTA BRIGADEIRO": "8316",
  "TORTA CHOC MORANGO": "8434",
  "TORTA CHOCOLATE": "8299",
  "TORTA DE FRANGO": "3302",
  "TORTA DOCE DE LEITE": "8425",
  "TORTA LEITE EM PÓ": "8310",
  "TORTA LEITE EM PÓ COM MORANGO": "8314",
  "TORTA MESCLADA": "8306",
  "TORTELA DE MORANGO": "80",
  "TORTELETE DE LIMÃO": "958"
}

# Criamos uma lista "limpa" para o bot ignorar acentos na busca exata
# Exemplo: se você digitar "pao", ele acha "PÃO"
PRODUTOS_BUSCA = {unidecode(k).lower(): (k, v) for k, v in PRODUTOS.items()}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi! Digite o nome do produto para o código. 🥐")

async def buscar_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Transforma o que você digitou (tira acento e deixa minúsculo)
    entrada = unidecode(update.message.text.lower().strip())

    if entrada in PRODUTOS_BUSCA:
        nome_real, codigo = PRODUTOS_BUSCA[entrada]
        await update.message.reply_text(f"✅ {nome_real}: {codigo}")
    else:
        # Mensagem curta se não for exato
        await update.message.reply_text("❌ Produto não encontrado.")

def main():
    if not TOKEN:
        return
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_codigo))
    application.run_polling()

if __name__ == '__main__':
    main()