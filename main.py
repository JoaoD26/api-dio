import pandas as pd
import openai as ai
import config
import time

#Extrair
df = pd.read_csv('dados.csv')
usuario = df['User_ID']
df['Oferta'] = df['Oferta'].astype(str)

def offer(saldo):
    
    saldo = saldo.replace("R$", "")
    saldo = saldo.replace(".", "")
    saldo = saldo.replace(",", ".")
    saldof = float(saldo)

    msg = ""

    if saldof >= 250000:
        msg = 'convite para conta premium, para eventos exclusivos ou para serviços personalizados de concierge'
    elif saldof >= 100000:
        msg = 'convite para programa de fidelidade personalizado ou recompensas de indicação'
    elif saldof >= 50000:
        msg = 'análise financeira gratuita ou serviços de planejamento financeiro'
    elif saldof >= 25000:
        msg = 'microempréstimos, linhas de crédito ou educação financeira'
    else:
        msg = 'programa de economia automatica ou cursos de educação financeira'
    
    return msg

#Transformar
ai.api_key = config.key

def generate_offer(user):
    saldo = df.loc[df['User_ID'] == user, 'Saldo'].values[0]
    nome = df.loc[df['User_ID'] == user, 'User'].values[0]
    msg = offer(saldo)
    completion = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um especialista em marketing bancário."},
            {"role": "user", "content": f"crie uma mensagem para {nome} com o tema {msg}, com no máximo 100 caracteres, e sempre coloque o nome na mensagem"}
        ]
    )
    time.sleep(10)

    return completion.choices[0].message.content.strip('\"')



for user in usuario:
    oferta = generate_offer(user)
#Carregar

    df.loc[df['User_ID'] == user, 'Oferta'] = oferta

df.to_csv('dados.csv', index=False)
