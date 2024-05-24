from flask import Flask, render_template,jsonify, request, Markup, url_for
import numpy as np
import pandas as pd

app = Flask(__name__)


# Load fertilizer recommendations
fertilizer_dic = {
    'NHigh': {
        'message': "Apply nitrogen-rich fertilizer in moderation.",
        'suggestions': [
            "Adding Manure is one of the simplest ways to amend your soil with nitrogen. Be careful as there are various types of manures with varying degrees of nitrogen.",
            "Use your morning addiction to feed your gardening habit! Coffee grounds in soil will be fed with nitrogen. An added benefit to including coffee grounds to your soil is while it will compost, it will also help provide increased drainage to your soil.",
            "Planting vegetables that are in Fabaceae family like peas, beans, and soybeans have the ability to increase nitrogen in your soil.",
            "Plant ‘green manure’ crops like cabbage, corn, and broccoli.",
            "Use mulch (wet grass) while growing crops. Mulch can also include sawdust and scrap softwoods."
        ]
    },
    'PHigh': {
        'message': "Apply phosphorus-rich fertilizer in moderation.",
        'suggestions': [
            "Avoid adding manure as it contains high levels of phosphorus.",
            "Use only phosphorus-free fertilizer.",
            "Soaking your soil liberally will aid in driving phosphorus out of the soil."
        ]
    },
    'KHigh': {
        'message': "Apply potassium-rich fertilizer in moderation.",
        'suggestions': [
            "Loosen the soil deeply with a shovel, and water thoroughly to dissolve water-soluble potassium. Allow the soil to fully dry, and repeat digging and watering the soil two or three more times.",
            "Sift through the soil and remove as many rocks as possible, using a soil sifter. Minerals occurring in rocks such as mica and feldspar slowly release potassium into the soil slowly through weathering.",
            "Stop applying potassium-rich commercial fertilizer. Apply only commercial fertilizer that has a '0' in the final number field. Commercial fertilizers use a three-number system for measuring levels of nitrogen, phosphorus, and potassium. The last number stands for potassium.",
            "Mix crushed eggshells, crushed seashells, wood ash, or soft rock phosphate into the soil to add calcium. Mix in up to 10 percent of organic compost to help amend and balance the soil."
        ]
    },
    'Nlow': {
        'message': "Increase nitrogen in soil.",
        'suggestions': [
            "Add Sawdust or fine woodchips to your soil. The carbon in the sawdust/woodchips loves nitrogen and will help absorb and soak up any excess nitrogen.",
            "Plant heavy nitrogen-feeding plants like tomatoes, corn, broccoli, cabbage, and spinach.",
            "Soaking your soil with water will help leach the nitrogen deeper into your soil, effectively leaving less for your plants to use.",
            "In limited studies, it was shown that adding sugar to your soil can help potentially reduce the amount of nitrogen in your soil. Sugar is partially composed of carbon, an element that soaks up nitrogen in the soil.",
            "Add composted manure to the soil.",
            "Plant Nitrogen-fixing plants like peas or beans.",
            "Use MPK fertilizers with high N value.",
            "Avoid over-fertilization as it can lead to nutrient imbalances, environmental pollution, and long-term soil degradation."
        ]
    },
    'Plow': {
        'message': "Increase phosphorus in soil.",
        'suggestions': [
            "Bone meal: A fast-acting source rich in phosphorus.",
            "Rock phosphate: A slower-acting source that needs to be converted by the soil.",
            "Apply fertilizer with a high phosphorus content.",
            "Adding quality organic compost to your soil will increase phosphorus content.",
            "Manure can be an excellent source of phosphorus for your plants.",
            "Introducing clay particles into your soil can help retain phosphorus.",
            "Ensure proper soil pH: Maintain a pH in the 6.0 to 7.0 range for optimal phosphorus uptake."
        ]
    },
    'Klow': {
        'message': "Increase potassium in soil.",
        'suggestions': [
            "Mix in muricate of potash or sulphate of potash.",
            "Try kelp meal or seaweed.",
            "Try Sul-Po-Mag."
        ]
    }
}


@app.route('/')
def index():
    return jsonify({"message" :"Server Started"})


@app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'Harvestify - Fertilizer Suggestion'

    # Preprocess crop name
    crop_name = request.json['crop'].strip().lower()

    # Read fertilizer data from a CSV file
    df = pd.read_csv('./Data/fertilizer.csv')

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
        N = int(request.json['N'])
        P = int(request.json['P'])
        K = int(request.json['K'])

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

        return jsonify({"message" :"Recommendation Successfully","recommendation":recommendation})
    else:
        # Handle the case where no rows match the condition
        return render_template('fert_Result.html', recommendation="No fertilizer recommendation found for the selected crop.", title=title)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5632)

