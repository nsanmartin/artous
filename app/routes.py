import pandas as pd
from urllib.parse import urlparse

from flask import render_template, redirect, request, url_for

from app import app
from app.forms import PriceForm

from timba.src import cache, fetch
from timba.scraping.www_rava_com__ \
    import response_mapping_cotizaciones_dolares as response_mapping

import re
float_regexp = re.compile('^(\d+(?:\.\d+)?)[mMkK]?$')

# todo: put this in timba
url = 'https://www.rava.com/cotizaciones/dolares'
expiration = 60*1000

def get_dolar_prices_for(pesos):
    rava = cache.fetch_url(
        fetcher = fetch.FetchReqGet(url, headers={}),
        response_mapping = response_mapping,
        cache = cache.CacheMem(expiration),
        path = cache.url_to_cache_path(url)
    )

    df = pd.DataFrame(rava['body'])
    df = df.drop( df.columns.difference(['ultimo', 'especie']), axis=1)
    df['p/d'] = pesos/df['ultimo']

    return [{
        'name'  : urlparse(url).netloc,
        'data'  : pd.DataFrame.to_html(df),
    }]


def parse_price(p):
    # double check, regex + float()
    if p and float_regexp.match(p):
        try:
            return(float(p))
        except ValueError:
            try:
                if p.endswith("k") or p.endswith("K"):
                    return(float(p[:-1]) * 1000)
                if p.endswith("m") or p.endswith("M"):
                    return(float(p[:-1]) * 1000000)
            except ValueError:
                pass
    return None

@app.route('/', methods=['GET'])
def price():
    form = PriceForm()
    priceq = request.args.get('price')
    parsed_price = parse_price(priceq)
    if parsed_price:
        data = get_dolar_prices_for(parsed_price)
        return render_template(
            'precio.html',
            title='Home',
            form=form,
            data=data,
            price=str(parsed_price)
        )
    else:
        return render_template('precio.html',  title='Precio', form=form)

