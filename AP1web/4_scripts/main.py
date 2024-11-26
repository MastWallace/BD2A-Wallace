from flask import Flask, jsonify
import pandas as pd
from collections import OrderedDict
import matplotlib as plb


app = Flask(__name__)


@app.route('/PCs/')
def get_metrics():
    dados = pd.read_csv('2_insights./base_pichau_pronta.csv')
    
    metrics = {
        'mean': dados['precos'].mean(),
        'median': dados['precos'].median(),
        'std_dev': dados['precos'].std()
    }

    return jsonify({
        'data': dados.to_dict(orient='records'),
        'metrics': metrics
    })

app.run(debug=True)


