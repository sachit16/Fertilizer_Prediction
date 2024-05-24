from flask import Flask, render_template, request, Markup, url_for
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)


# Load fertilizer recommendations
fertilizer_dic = {
    'NHigh': """<center><h2>Apply nitrogen-rich fertilizer in moderation.</h3><br>
               <h3>Suggestions:</h3></center>
               <ol>
                   <li><i>Manure:</i> Adding Manure is one of the simplest ways to amend your soil with nitrogen. <br>Be careful as there are various types of manures with varying degrees of nitrogen.</li>
                   <br> <li><i>Coffee grinds:</i> Use your morning addiction to feed your gardening habit! Coffee grounds in soil will be fed with nitrogen. An added benefit to including coffee grounds to your soil is while it will compost, it will also help provide increased drainage to your soil.</li>
                   <br> <li><i>Plant nitrogen fixing plants:</i> Planting vegetables that are in Fabaceae family like peas, beans, and soybeans have the ability to increase nitrogen in your soil.</li>
                   <br><li><i>Plant ‘green manure’ crops:</i> Like cabbage, corn, and broccoli.</li>
                   <br><li><i>Use mulch (wet grass) while growing crops:</i> Mulch can also include sawdust and scrap softwoods.</li>
               </ol>""",
    'PHigh': """<center><h2>Apply phosphorus-rich fertilizer in moderation.</h2><br>
                <h3>Suggestions:</h2><center>
                <ol>
                    <li><i>Avoid adding manure:</i> Manure contains high levels of phosphorus.</li>
                    <br><li><i>Use only phosphorus-free fertilizer:</i> Find a fertilizer with no phosphorus.</li>
                    <br><li><i>Water your soil:</i> Soaking your soil liberally will aid in driving phosphorus out of the soil.</li>
                </ol>""",
    'KHigh': """<center><h2>Apply potassium-rich fertilizer in moderation.</h2><br>
                <h3>Suggestions:</h3></center>
                <ol>
                    <li><i>Loosen the soil:</i> Deeply with a shovel, and water thoroughly to dissolve water-soluble potassium.<br/> Allow the soil to fully dry, and repeat digging and watering the soil two or three more times.</li>
                    <br><li><i>Sift through the soil:</i> And remove as many rocks as possible, using a soil sifter. Minerals occurring in rocks such as mica and feldspar slowly release potassium into the soil slowly through weathering.</li>
                    <br><li><i>Stop applying potassium-rich commercial fertilizer:</i> Apply only commercial fertilizer that has a '0' in the final number field. Commercial fertilizers use a three-number system for measuring levels of nitrogen, phosphorus, and potassium. The last number stands for potassium.</li>
                    <br><li><i>Mix crushed eggshells, crushed seashells, wood ash, or soft rock phosphate into the soil:</i> To add calcium. Mix in up to 10 percent of organic compost to help amend and balance the soil.</li>
                </ol>""",
    'Nlow': """<center><h2>Increase nitrogen in soil.</h2><br>
               <h3>Suggestions:</h3></center>
               <ol>
                   <li><i>Add Sawdust or fine woodchips to your soil:</i> The carbon in the sawdust/woodchips loves nitrogen and will help absorb and soak up any excess nitrogen.</li>
                   <br><li><i>Plant heavy nitrogen-feeding plants:</i> Like tomatoes, corn, broccoli, cabbage, and spinach.</li>
                   <br><li><i>Water your soil:</i> Soaking your soil with water will help leach the nitrogen deeper into your soil, effectively leaving less for your plants to use.</li>
                   <br><li><i>Sugar:</i> In limited studies, it was shown that adding sugar to your soil can help potentially reduce the amount of nitrogen in your soil. Sugar is partially composed of carbon, an element that soaks up nitrogen in the soil.</li>
                   <br><li><i>Add composted manure to the soil.</i></li>
                   <br><li><i>Plant Nitrogen-fixing plants:</i> Like peas or beans.</li>
                   <br><li><i>Use MPK fertilizers with high N value.</i></li>
                   <br><li><i>Do nothing:</i> While it may seem counter-intuitive, avoid over-fertilization as it can lead to nutrient imbalances, environmental pollution, and long-term soil degradation.</li>
               </ol>""",
    'Plow': """<center><h2>Increase phosphorus in soil.</h2><br>
               <h3>Suggestions:</h3></center>
               <ol>
                   <li><i>Bone meal:</i> A fast-acting source rich in phosphorus.</li>
                   <br><li><i>Rock phosphate:</i> A slower-acting source that needs to be converted by the soil.</li>
                   <br><li><i>Phosphorus fertilizers:</i> Apply fertilizer with a high phosphorus content.</li>
                   <br><li><i>Organic compost:</i> Adding quality organic compost to your soil will increase phosphorus content.</li>
                   <br><li><i>Manure:</i> Manure can be an excellent source of phosphorus for your plants.</li>
                   <br><li><i>Clay soil:</i> Introducing clay particles into your soil can help retain phosphorus.</li>
                   <br>li><i>Ensure proper soil pH:</i> Maintain a pH in the 6.0 to 7.0 range for optimal phosphorus uptake.</li>
               </ol>""",
    'Klow': """<center><h2>Increase potassium in soil.</h2><br>
               <h3>Suggestions:</h3></center>
               <ol>
                   <li><i>Mix in muricate of potash or sulphate of potash.</i></li>
                   <br><li><i>Try kelp meal or seaweed.</i></li>
                   <br><li><i>Try Sul-Po-Mag.</i></li>
               </ol>"""
}

@app.route('/')
def index():
    return render_template('fertilizer.html')


@app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'Harvestify - Fertilizer Suggestion'

    # Preprocess crop name
    crop_name = request.form['crop'].strip().lower()

    # Read fertilizer data from a CSV file
    df = pd.read_csv('Data/fertilizer.csv')

    # Convert crop names in the DataFrame to lowercase and remove extra whitespace
    df['Crop'] = df['Crop'].str.strip().str.lower()

    # Filter the DataFrame based on the preprocessed crop name
    filtered_df = df[df['Crop'] == crop_name]

    if not filtered_df.empty:
        # Get recommended N, P, K values for the specified crop
        nr = filtered_df['N'].iloc[0]
        pr = filtered_df['P'].iloc[0]
        kr = filtered_df['K'].iloc[0]

        # User input for N, P, K
        N = int(request.form['N'])
        P = int(request.form['P'])
        K = int(request.form['K'])

        # Calculate differences between user-input and recommended N, P, K values
        n_diff = nr - N
        p_diff = pr - P
        k_diff = kr - K

        # Identify the nutrient with the largest difference
        temp = {abs(n_diff): "N", abs(p_diff): "P", abs(k_diff): "K"}
        max_value = temp[max(temp.keys())]

        # Select fertilizer recommendation based on the identified nutrient
        if max_value == "N":
            key = 'NHigh' if n_diff < 0 else 'Nlow'
        elif max_value == "P":
            key = 'PHigh' if p_diff < 0 else 'Plow'
        else:
            key = 'KHigh' if k_diff < 0 else 'Klow'

        # Get the fertilizer recommendation
        recommendation = fertilizer_dic[key]

        return render_template('fert_Result.html', recommendation=recommendation, title=title)
    else:
        # Handle the case where no rows match the condition
        return render_template('fert_Result.html', recommendation="No fertilizer recommendation found for the selected crop.", title=title)

if __name__ == '__main__':
    app.run(debug=True)
