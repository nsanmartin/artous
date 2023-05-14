import pandas as pd
from app import app
from timba.src import cache
from timba.scraping.www_rava_com__ \
    import response_mapping_cotizaciones_dolares as response_mapping

# todo: put this in timba
url = 'https://www.rava.com/cotizaciones/dolares'
expiration = 60*10


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/<int:num>')
def artous(num):
    try:
        precio = float(num)

        try:
            rava = cache.fetch_url_get(
                url=url,
                headers={},
                response_mapping=response_mapping,
                expiration=expiration
            )
            df = pd.DataFrame(rava['body'])
            df = df.drop(
                df.columns.difference(['ultimo', 'especie']), axis=1
            )

            df['p/d'] = precio/df['ultimo']

            return pd.DataFrame.to_html(df)

        except Exception as e:
            #todoL don't do this jaja
            return str(e)


    except:
        return 'bad number!', 400
